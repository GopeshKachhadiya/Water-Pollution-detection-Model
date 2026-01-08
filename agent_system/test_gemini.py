import os
from google import genai
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# ✅ CREATE CLIENT (THIS WAS MISSING)
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# Test prompt
response = client.models.generate_content(
    model="models/gemini-flash-latest",
    contents="Say exactly: Gemini is working."
)

# Print response safely
print(response.candidates[0].content.parts[0].text)
