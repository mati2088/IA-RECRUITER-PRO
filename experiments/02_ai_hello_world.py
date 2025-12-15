"""
02_ai_hello_world.py
Tu primera interacción con una IA usando LangChain.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

# 1. Cargar variables de entorno (.env)
load_dotenv()

# 2. Configurar el modelo (LLM)
# Usamos 'gemini-pro' (equivalente a GPT-3.5/4)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0.7)

def main():
    print("🤖 Conectando con Gemini...")

    # 3. Crear los mensajes
    # SystemMessage: Define el rol o personalidad
    # HumanMessage: Lo que tú le dices
    messages = [
        SystemMessage(content="Eres un asistente experto en QA Automation que habla con metáforas de testing."),
        HumanMessage(content="Explícame qué es la Inteligencia Artificial en una frase corta.")
    ]

    # 4. Invocar al modelo
    response = llm.invoke(messages)

    # 5. Mostrar la respuesta
    print("\n--- Respuesta de la IA ---")
    print(response.content)
    print("--------------------------")

if __name__ == "__main__":
    main()
