# 🤖 AI Recruiter Assistant

Una herramienta inteligente desarrollada en **Python** que actúa como un Asistente de RRHH.
Permite subir múltiples currículums (PDF), leerlos automáticamente y chatear con una IA para encontrar al candidato ideal basándose en tus requerimientos.

## 🚀 Características
- **Análisis de CVs**: Lectura automática de archivos PDF.
- **Chat Conversacional**: Pregunta sobre los candidatos en lenguaje natural.
- **RAG (Retrieval Augmented Generation)**: La IA tiene "memoria" del contenido de los CVs.
- **Tech Stack**: 
    - [Streamlit](https://streamlit.io/) (Frontend)
    - [LangChain](https://langchain.com/) (Orquestación)
    - [Google Gemini](https://ai.google.dev/) (Modelo LLM: `gemini-2.5-flash`)

## 🛠️ Instalación

1. **Clonar/Descargar** este repositorio.
2. **Crear entorno virtual** (si no existe):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
3. **Instalar dependencias**:
   ```powershell
   pip install -r requirements.txt
   ```
   *(Nota: Si no tienes requirements.txt, usa: `pip install streamlit pypdf langchain-google-genai python-dotenv`)*

4. **Configurar API Key**:
   - Crea un archivo `.env` en la raíz.
   - Añade tu clave de Google AI Studio:
     ```
     GOOGLE_API_KEY=tu_clave_aqui
     ```

## ▶️ Ejecución

Para iniciar la aplicación:

```powershell
streamlit run src/app.py
```

La app se abrirá automáticamente en tu navegador (usualmente `http://localhost:8501`).

## 📂 Estructura del Proyecto

- `src/`: Código fuente de la aplicación (`app.py`).
- `experiments/`: Scripts de prueba y aprendizaje.
- `docs/`: Documentación y Roadmap.
