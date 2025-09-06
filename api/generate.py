import os
import json
import uuid
import io
import requests
import base64
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Env vars (set in Vercel dashboard)
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

def handler(request):
    # Log request
    print(f"Request received: {request}")

    # Parse query params
    try:
        prompt = request.get('query', {}).get('prompt', '')
        if not prompt:
            print("Error: Missing prompt")
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Missing prompt parameter'})
            }
    except Exception as e:
        print(f"Error parsing request: {str(e)}")
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'Invalid request: {str(e)}'})
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
            model="llama3-8b-8192",  # Confirmed Groq model
            messages=[
                {
                    "role": "user",
                    "content": f"You are a Diagram Architect AI. Generate clean Mermaid flowchart code for: '{prompt}'. Focus on visual, image-like full-chart style for chemistry (e.g., nodes with formulas like H₂O, arrows for reactions). Output ONLY the Mermaid code wrapped in ```mermaid ... ```. Example: ```mermaid graph TD; A[Start] --> B[Process]; B --> C[End]; ```"
                }
            ],
            temperature=1,
            max_tokens=8192,  # Updated to max_tokens (Groq standard)
            top_p=1,
            stream=False,
            stop=None
        )

        # Extract Mermaid code
        mermaid_code = completion.choices[0].message.content.strip()
        print(f"Raw Groq output: {mermaid_code}")
        if '```mermaid' in mermaid_code:
            mermaid_code = mermaid_code.split('```mermaid')[1].split('```')[0].strip()
        elif 'graph TD' in mermaid_code or 'graph LR' in mermaid_code:
            lines = mermaid_code.split('\n')
            mermaid_code = '\n'.join(line for line in lines if 'graph TD' in line or 'graph LR' in line or '-->' in line or '[' in line).strip()
        else:
            print("Error: Invalid Mermaid output")
            raise ValueError("Invalid or empty Mermaid code from Groq")

        if not mermaid_code:
            print("Error: Empty Mermaid code")
            raise ValueError("Empty Mermaid code generated")

        # Step 2: Render Mermaid to PNG with Kroki
        kroki_url = "https://kroki.io"
        response = requests.post(
            f"{kroki_url}/mermaid/png",
            data=mermaid_code.encode('utf-8'),
            headers={'Content-Type': 'text/plain'}
        )
        print(f"Kroki response status: {response.status_code}")
        if response.status_code != 200:
            print(f"Kroki error: {response.text}")
            raise ValueError(f"Kroki rendering failed: {response.text}")
        image_bytes = response.content

        # Step 3: Upload to ImgBB
        imgbb_url = "https://api.imgbb.com/1/upload"
        image_b64 = base64.b64encode(image_bytes).decode('utf-8')
        payload = {
            'image': image_b64,
            'name': f"flowchart-{uuid.uuid4().hex[:8]}"
        }
        imgbb_response = requests.post(imgbb_url, data=payload)
        print(f"ImgBB response status: {imgbb_response.status_code}")
        if imgbb_response.status_code != 200:
            print(f"ImgBB error: {imgbb_response.text}")
            raise ValueError(f"ImgBB upload failed: {imgbb_response.text}")
        imgbb_data = imgbb_response.json()
        image_url = imgbb_data['data']['url']

        # Step 4: Return JSON
        print(f"Success: Image URL: {image_url}")
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'image_url': image_url, 'mermaid_code': mermaid_code})
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': f"Server error: {str(e)}"})
        }
