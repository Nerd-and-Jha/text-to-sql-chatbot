import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"API Key found: {api_key[:10]}...")

genai.configure(api_key=api_key)

# Try to list models
print("\nAvailable models:")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"  - {model.name}")

# Try to use the model
print("\nTesting model...")
model = genai.GenerativeModel('gemini-2.5-flash')
response = model.generate_content("Say hello")
print(f"Response: {response.text}")