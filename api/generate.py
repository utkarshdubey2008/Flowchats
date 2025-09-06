import os
import json
import uuid
import requests
import base64
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Env vars (set in Vercel dashboard)
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

def handler(request, context):  # Note: Added context parameter
    # Handle different request formats
    if hasattr(request, 'args'):
        # Vercel request object
        prompt = request.args.get('prompt', '')
    elif isinstance(request, dict):
        # Direct dict (for testing)
        prompt = request.get('prompt', '')
    else:
        # Try to get from query params
        prompt = getattr(request, 'args', {}).get('prompt', '') or ''
    
    print(f"Request received, prompt: {prompt}")

    # Validate prompt
    if not prompt:
        print("Error: Missing prompt")
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Missing prompt parameter'})
        }

    # Verify API key
    if not GROQ_API_KEY:
        print("Error: GROQ_API_KEY not set")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Server configuration error: Missing API key'})
        }

    try:
        # Step 1: Generate Mermaid flowchart code with Groq
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "user",
                    "content": f"You are a Diagram Architect AI. Generate clean Mermaid flowchart code for: '{prompt}'. Focus on visual, image-like full-chart style for chemistry (e.g., nodes with formulas like H₂O, arrows for reactions). Output ONLY the Mermaid code wrapped in ```mermaid ... ```. Example: ```mermaid graph TD; A[Start] --> B[Process]; B --> C[End]; ```"
                }
            ],
            temperature=1,
            max_tokens=8192,
            top_p=1,
            stream=False,
            stop=None
        )

        # Extract Mermaid code
        mermaid_code = completion.choices[0].message.content.strip()
        print(f"Raw Groq output: {mermaid_code}")
        
        # Clean up the mermaid code
        if '```mermaid' in mermaid_code:
            mermaid_code = mermaid_code.split('```mermaid')[1].split('```')[0].strip()
        elif '```' in mermaid_code:
            # Handle case where it's just wrapped in ```
            parts = mermaid_code.split('```')
            for part in parts:
                if 'graph' in part or 'flowchart' in part:
                    mermaid_code = part.strip()
                    break
        
        # Validate we have valid mermaid code
        if not mermaid_code or not any(keyword in mermaid_code.lower() for keyword in ['graph', 'flowchart', '-->']):
            print("Error: Invalid Mermaid output")
            raise ValueError("Invalid or empty Mermaid code from Groq")

        print(f"Cleaned Mermaid code: {mermaid_code}")

        # Step 2: Render Mermaid to PNG with Kroki
        kroki_url = "https://kroki.io"
        try:
            response = requests.post(
                f"{kroki_url}/mermaid/png",
                data=mermaid_code.encode('utf-8'),
                headers={'Content-Type': 'text/plain'},
                timeout=30  # Add timeout
            )
            print(f"Kroki response status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"Kroki error: {response.text}")
                raise ValueError(f"Kroki rendering failed: HTTP {response.status_code}")
                
            image_bytes = response.content
            if not image_bytes:
                raise ValueError("Kroki returned empty image")
                
        except requests.exceptions.RequestException as e:
            print(f"Kroki request error: {str(e)}")
            raise ValueError(f"Failed to connect to Kroki: {str(e)}")

        # Step 3: Upload to ImgBB (only if you have API key)
        imgbb_api_key = os.getenv('IMGBB_API_KEY')
        if not imgbb_api_key:
            # Return base64 encoded image instead
            image_b64 = base64.b64encode(image_bytes).decode('utf-8')
            image_url = f"data:image/png;base64,{image_b64}"
        else:
            imgbb_url = f"https://api.imgbb.com/1/upload?key={imgbb_api_key}"
            image_b64 = base64.b64encode(image_bytes).decode('utf-8')
            payload = {
                'image': image_b64,
                'name': f"flowchart-{uuid.uuid4().hex[:8]}"
            }
            
            try:
                imgbb_response = requests.post(imgbb_url, data=payload, timeout=30)
                print(f"ImgBB response status: {imgbb_response.status_code}")
                
                if imgbb_response.status_code != 200:
                    print(f"ImgBB error: {imgbb_response.text}")
                    # Fallback to base64
                    image_url = f"data:image/png;base64,{image_b64}"
                else:
                    imgbb_data = imgbb_response.json()
                    image_url = imgbb_data['data']['url']
                    
            except requests.exceptions.RequestException as e:
                print(f"ImgBB request error: {str(e)}")
                # Fallback to base64
                image_url = f"data:image/png;base64,{image_b64}"

        # Step 4: Return JSON
        print(f"Success: Image URL generated")
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',  # Add CORS headers
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                'image_url': image_url, 
                'mermaid_code': mermaid_code,
                'success': True
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': f"Server error: {str(e)}",
                'success': False
            })
        }
