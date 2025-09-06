import os
import json
import uuid
import io
import requests
import base64
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Env vars (set in Vercel)
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

def handler(request):
    # Parse query params (Vercel sends as dict)
    prompt = request.get('query', {}).get('prompt', '')
    if not prompt:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Missing prompt parameter'})
        }

    try:
        # Step 1: Use Groq to generate Mermaid flowchart code (Diagram Architect agent)
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",  # Your specified model
            messages=[
                {
                    "role": "user",
                    "content": f"You are a Diagram Architect AI. Generate clean Mermaid flowchart code for: '{prompt}'. Focus on visual, image-like full-chart style for chemistry (e.g., nodes with formulas like H₂O, arrows for reactions). Output ONLY the Mermaid code wrapped in ```mermaid ... ```. Example: ```mermaid graph TD; A[Start] --> B[Process]; B --> C[End]; ```"
                }
            ],
            temperature=1,
            max_completion_tokens=8192,
            top_p=1,
            reasoning_effort="medium",
            stream=False,  # Non-streaming for API simplicity
            stop=None
        )

        # Extract Mermaid code
        mermaid_code = completion.choices[0].message.content.strip()
        if '```mermaid' in mermaid_code:
            mermaid_code = mermaid_code.split('```mermaid')[1].split('```')[0].strip()
        else:
            raise ValueError("Invalid Mermaid output")

        # Step 2: Render Mermaid to PNG using Kroki.io (free, no key)
        kroki_url = "https://kroki.io"
        response = requests.post(
            f"{kroki_url}/mermaid/png",
            data=mermaid_code,
            headers={'Content-Type': 'text/plain'}
        )
        if response.status_code != 200:
            raise ValueError("Kroki rendering failed")
        image_bytes = response.content

        # Step 3: Upload to ImgBB (no API key needed)
        imgbb_url = "https://api.imgbb.com/1/upload"
        image_b64 = base64.b64encode(image_bytes).decode('utf-8')
        payload = {
            'image': image_b64,
            'name': f"flowchart-{uuid.uuid4().hex[:8]}"
        }
        imgbb_response = requests.post(imgbb_url, data=payload)
        if imgbb_response.status_code != 200:
            raise ValueError("ImgBB upload failed")
        imgbb_data = imgbb_response.json()
        image_url = imgbb_data['data']['url']

        # Step 4: Return JSON with image link
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'image_url': image_url, 'mermaid_code': mermaid_code})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

# For local testing
if __name__ == "__main__":
IBE0
    class MockRequest:
        def get(self, key):
            if key == 'query':
                return {'prompt': 'generate a flowchart for chemistry chemical formulas'}
    print(json.loads(handler(MockRequest())['body']))
