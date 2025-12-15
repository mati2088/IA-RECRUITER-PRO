import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("--- SEARCHING FOR 1.5 MODELS ---")
for m in genai.list_models():
    if "1.5" in m.name and "generateContent" in m.supported_generation_methods:
        print(f"✅ DETECTED: {m.name}")
print("--------------------------------")
