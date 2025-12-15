"""
03_gemini_raw.py
Prueba directa con el SDK de Google (sin LangChain) para descartar errores.
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"🔑 Key detectada: {api_key[:10]}...")

genai.configure(api_key=api_key)

try:
    # Listar modelos disponibles para ver cuál tenemos acceso
    print("📋 Buscando modelos disponibles...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f" - {m.name}")

    print("\n🤖 Intentando generar contenido con 'gemini-1.5-flash'...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Hola, ¿funcionas?")
    print(f"\n✅ RESPUESTA: {response.text}")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
