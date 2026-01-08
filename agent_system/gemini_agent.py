from dotenv import load_dotenv
load_dotenv()

import os
from google import genai

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

def run_agent(detection_payload: dict) -> str:
    prompt = f"""
You are an environmental intelligence AI agent.

Analyze the following water pollution detection data and provide:
1. Severity level (Low / Medium / High)
2. Environmental impact
3. place responsible for this like factory or tourist place
4. authority under this area
Detection data:
{detection_payload}
"""

    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt
    )

    return response.candidates[0].content.parts[0].text
