import streamlit as st
import os
import time
import pandas as pd
import json
import unicodedata
import base64
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

# Helper para limpiar texto (sin acentos)
def remove_accents(input_str):
    if not isinstance(input_str, str): return input_str
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

# 1. Configuración Global
st.set_page_config(page_title="IA Recruiter Pro", page_icon="🚀", layout="wide")
load_dotenv()

# --- Gestión de Estado ---
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# --- Lógica de Negocio ---
def get_bg_image_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        try:
            pdf_reader = PdfReader(pdf)
            file_content = ""
            for page in pdf_reader.pages:
                file_content += page.extract_text()
            text += f"\n--- INICIO CV: {pdf.name} ---\n{file_content}\n--- FIN CV ---\n"
        except: pass
    return text

def get_ai_response(messages_history):
    # Prioridad: Clave del usuario > Clave del sistema (.env)
    user_key = st.session_state.get('user_api_key')
    api_key = user_key if user_key else os.getenv("GOOGLE_API_KEY")
    
    # Forzamos JSON output
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0.2, 
        api_key=api_key,
        max_retries=3
    )
    return llm.invoke(messages_history).content

def parse_json_response(response_text):
    """Limpia el markdown ```json ... ``` si existe"""
    try:
        clean_text = response_text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except Exception as e:
        return None

def validate_key_connection(api_key):
    """Prueba rápida de conectividad con la Key"""
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key)
        llm.invoke("test")
        return True, "OK"
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            return False, "⏳ Tu API Key es válida pero ha excedido su CUOTA GRATUITA. Intenta con otra o espera."
        elif "400" in error_msg or "INVALID_ARGUMENT" in error_msg:
            return False, "❌ La API Key es incorrecta o no existe."
        else:
            return False, f"❌ Error de conexión: {error_msg}"

# --- Vistas ---
def show_login():
    # Fondo Profesional con Imagen Local y Card Azul
    try:
        bg_image = get_bg_image_base64("assets/login_bg.jpg")
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{bg_image}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            
            /* Overlay oscuro general */
            .stApp::before {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.4);
                z-index: -1;
            }}
            
            /* --- ESTILO CARD AZUL (Columna Central) --- */
            /* Intentamos varios selectores para asegurar compatibilidad */
            div[data-testid="stColumn"]:nth-of-type(2), 
            div[data-testid="column"]:nth-of-type(2) {{
                background-color: #1e3c72; /* Azul sólido */
                background-image: linear-gradient(135deg, rgba(30, 60, 114, 0.95) 0%, rgba(42, 82, 152, 0.95) 100%);
                padding: 3rem !important;
                border-radius: 20px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}

            /* Inputs */
            .stTextInput > div > div {{
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            .stTextInput > div > div:focus-within {{
                border-color: #4facfe;
                box-shadow: 0 0 10px rgba(79, 172, 254, 0.5);
            }}

            /* Labels */
            .stTextInput > label {{
                color: white !important;
                font-size: 1.1rem !important;
                font-weight: 600 !important;
            }}
            
            /* Headers y Textos */
            div[data-testid="stMarkdownContainer"] > h2 {{
                color: white !important;
                text-align: center;
                font-weight: 700;
                margin-bottom: 0.5rem;
            }}
            .stAlert {{
                background-color: rgba(220, 53, 69, 0.8) !important; /* Rojo corporativo */
                color: white !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
            }}
            div[data-testid="stMarkdownContainer"] > p {{
                color: #f0f0f0 !important;
            }}
            
            /* Botón */
            .stButton > button {{
                width: 100%;
                background: linear-gradient(to right, #00c6ff, #0072ff);
                color: white;
                font-weight: bold;
                border: none;
                padding: 0.5rem 1rem;
                transition: transform 0.2s;
            }}
            .stButton > button:hover {{
                transform: scale(1.02);
                box-shadow: 0 5px 15px rgba(0, 114, 255, 0.4);
            }}
            </style>
            """, unsafe_allow_html=True)
    except Exception:
         st.markdown("""<style>.stApp { background: #1e3c72; color: white; }</style>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,3,1]) 
    with col2:
        st.markdown("## 🔐 Acceso Corporativo")
        st.info("Para uso ilimitado, ingresa tu propia API Key de Google Gemini. Si no, usa la contraseña de invitado.")
        
        # Opción 1: BYOK
        user_key = st.text_input("Tu Gemini API Key (Opcional)", type="password", help="Obténla gratis en aistudio.google.com")
        
        # Opción 2: Password
        password = st.text_input("Contraseña de Invitado", type="password")
        
        st.write("") # Espacio
        if st.button("INGRESAR AL SISTEMA", type="primary"):
            if user_key:
                # 1. Validar Key
                with st.spinner("Validando API Key con Google..."):
                    is_valid, msg = validate_key_connection(user_key)
                    if is_valid:
                        # 2. Guardar en session state
                        st.session_state['user_api_key'] = user_key
                        st.session_state.page = 'app'
                        st.success(f"✅ Key Válida. Bienvenido 🚀")
                        time.sleep(1)
                        # 3. Recargar
                        st.rerun()
                    else:
                        st.error(msg)
                
            elif password == "antigravity": 
                st.session_state['user_api_key'] = None # Usar system key
                st.session_state.page = 'app'
                st.success("Acceso concedido (Modo Invitado)")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Credenciales inválidas. Ingresa una API Key válida o la contraseña correcta.")

def show_app():
    st.title("🚀 IA Recruiter Dashboard")

    # Sidebar
    with st.sidebar:
        st.header("📂 Base de Conocimiento")
        pdf_docs = st.file_uploader("Cargar CVs", type="pdf", accept_multiple_files=True)
        if pdf_docs:
            with st.spinner("Indexando..."):
                raw_text = get_pdf_text(pdf_docs)
                st.session_state['cv_context'] = raw_text
                st.info(f"📚 {len(pdf_docs)} CVs cargados en memoria.")
        else:
            st.session_state['cv_context'] = ""
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Salir", key="btn_salir_sidebar"):
                st.session_state.clear()
                st.rerun()
        with col2:
            if st.button("Limpiar Chat", key="btn_limpiar_chat"):
                st.session_state.messages = [{"role": "assistant", "content": "Hola. Pásame la Job Description (JD) para analizar a tus candidatos."}]
                st.rerun()

    # Chat & Dashboard
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hola. Pásame la Job Description (JD) para analizar a tus candidatos."}]

    # Render mensajes previos
    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            # Si el contenido es un dict (JSON parseado), mostramos widgets
            if isinstance(msg["content"], dict) and "candidates" in msg["content"]:
                data = msg["content"]
                candidates = data['candidates']
                
                if candidates:
                    st.success(f"✅ Análisis Completado: {len(candidates)} Candidatos Viables")
                    
                    # 1. Tabla
                    df = pd.DataFrame(candidates)
                    st.dataframe(df, use_container_width=True)
                    
                    colA, colB = st.columns(2)
                    # 2. Exportar Excel (CSV Limpio)
                    with colA:
                        try:
                            # Limpiar acentos en todo el DF
                            df_clean = df.applymap(remove_accents)
                        except:
                            df_clean = df
                        
                        csv = df_clean.to_csv(index=False, sep=';').encode('utf-8')
                        st.download_button(
                            "📥 Descargar Reporte (CSV)", 
                            data=csv, 
                            file_name="reporte_rrhh.csv", 
                            mime="text/csv",
                            key=f"download_{i}"
                        )
                    
                    # 3. Análisis Detallado (Texto)
                    st.markdown("### 🔍 Detalles")
                    for c in candidates:
                        st.markdown(f"**{c['Nombre']}** ({c['Score']}%)")
                        st.caption(c['Reason'])
                else:
                    st.warning("⚠️ No se encontraron candidatos que coincidan con esta búsqueda en los CVs cargados.")
            else:
                st.markdown(msg["content"])

    # Input Usuario
    if prompt := st.chat_input("Escribe la JD o preguntas..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Prompt con Output Estructurado
        context = st.session_state.get('cv_context', '')
        full_prompt = f"""
        CONTEXTO (CVs): {context}
        JD USUARIO: {prompt}
        
        INSTRUCCIONES CLAVE:
        - Eres un RECLUTADOR experto.
        - Analiza los CVs.
        - TU SALIDA DEBE SER ÚNICAMENTE UN JSON VÁLIDO con esta estructura:
        {{
            "candidates": [
                {{
                    "Nombre": "Nombre real o archivo",
                    "Rol": "Titulo profesional",
                    "Score": 85 (numero entero 0-100),
                    "Ubicación": "Ciudad",
                    "Reason": "Breve justificación de por qué encaja o no"
                }}
            ]
        }}
        - Evalúa a TODOS los candidatos, incluso si el score es bajo.
        - NO escribas markdown antes ni después del JSON (solo el JSON).
        - Si no hay candidatos, devuelve lista vacía.
        """

        with st.chat_message("assistant"):
            with st.spinner("Analizando datos y generando reporte..."):
                try:
                    response_text = get_ai_response([SystemMessage(content="Eres un motor de análisis JSON."), HumanMessage(content=full_prompt)])
                    st.session_state['last_raw_response'] = response_text # Debug capture
                    
                    # Intentar parsear JSON
                    json_data = parse_json_response(response_text)
                    
                    if json_data:
                        # Guardar objeto estructurado en historial
                        st.session_state.messages.append({"role": "assistant", "content": json_data})
                        st.rerun() # Recargar para que el loop de render muestre los widgets
                    else:
                        # Fallback texto plano
                        st.markdown(response_text)
                        st.session_state.messages.append({"role": "assistant", "content": response_text})

                except Exception as e:
                    error_msg = str(e)
                    if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                        st.warning("⏳ **Límite de Velocidad Alcanzado (Error 429)**")
                        st.markdown("""
                        El servicio de IA gratuito de Google (Gemini) está saturado temporalmente.
                        
                        **Solución:**
                        1. Espera unos **10-20 segundos**.
                        2. Inténtalo de nuevo.
                        
                        *Nota: Para uso intensivo real, se requiere una API Key con facturación habilitada.*
                        """)
                    else:
                        st.error(f"❌ Error del Sistema: {e}")

# Router
if st.session_state.page == 'login':
    show_login()
else:
    show_app()
