"""
01_basics.py
Una introducción rápida a Python para desarrolladores Java/TS.
"""

import asyncio
from typing import List, Dict, Optional # Similar a Imports en Java/TS

# 1. Variables y Tipado (Dynamic but Strong)
# TS: const name: string = "Antigravity";
name: str = "Antigravity" 
age: int = 1

# 2. Estructuras de Datos
# TS: const skills: string[] = ["Java", "TS", "SQL"];
# Python Lists (Arrays dinámicos)
skills: List[str] = ["Java", "TS", "SQL"]
skills.append("Python") 

# TS: const user = { name: "User", role: "QA" };
# Python Dictionaries (Maps / Objects)
user_info: Dict[str, str] = {
    "name": "Nubiral",
    "role": "QA Automation Engineer"
}

# 3. List Comprehensions (Muy Pythonic - como .map() y .filter() combinados)
# TS: const shoutedSkills = skills.map(s => s.toUpperCase());
shouted_skills = [s.upper() for s in skills]

# 4. Funciones y Async
# TS: async function fetchData(): Promise<string> { ... }
async def fetch_data() -> str:
    print("Simulando llamada a API...")
    await asyncio.sleep(1) # Non-blocking sleep
    return "Datos recibidos de la IA"

# 5. Clases (Similar a Java/TS)
class Tester:
    def __init__(self, name: str): # Constructor
        self.name = name
    
    def test(self):
        print(f"{self.name} está ejecutando pruebas...")

# Main execution logic
# Java: public static void main(String[] args)
async def main():
    print(f"Hola {user_info['name']}!")
    print(f"Tus skills actualizados: {skills}")
    
    # Probando async
    data = await fetch_data()
    print(data)
    
    # Probando clases
    me = Tester("Nubiral")
    me.test()

if __name__ == "__main__":
    asyncio.run(main())
