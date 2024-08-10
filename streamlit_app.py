import streamlit as st
import os
import google.generativeai as genai
import time

# Set page config for a wider layout
st.set_page_config(page_title="Iset'Com Guide Chatbot", page_icon="🎓", layout="wide")

# Get API key from environment variable
api_key = os.getenv("API")
if api_key is None:
    st.error("Error: GEMINI_API_KEY environment variable is not set.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)

# Create the model
generation_config = {
    "temperature": 0.7,  # Adjust temperature for more focused responses
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 4096,  # Adjust as needed
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="""Reponds en francais , tunisien.
    Iset'Com se trouve au Technopole El Ghazela Tunis , siteweb: https://isetcom.tn/
    aYANT 2 Licences STIC et GTIC
    STIC : 3 semestres tronc commun et 3 semestres de specialite SR et RST
    GTIC : 6 semestres tronc commun.
    Les frais de scolarite sont fixés par l'ISET'Com de (70 - 82dt).

    """
)

# Predefined French questions
questions = [
    "Quelles sont les spécialités offertes à l'ISET'Com?",
    "Quels sont les frais de scolarité?",
    "Y a-t-il des programmes d'aide financière disponibles?",
    "Comment puis-je postuler à l'ISET'Com?",
    "Quelles sont les dates limites d'inscription?",
    "Où se trouve le campus de l'ISET'Com?",
    "Quels sont les débouchés professionnels après l'obtention du diplôme?",
    "Y a-t-il des clubs étudiants ou des activités parascolaires?",
    "L'ISET'Com propose-t-elle des programmes d'échange international?",
    "Comment puis-je contacter le service des admissions?",
    "Quels sont les scores des derniers étudiants admis à l'ISET'Com?" # New question
]


# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# --- Streamlit App UI ---
st.title("🎓 Iset'Com Guide Chatbot 🤖")
st.write("Posez des questions sur l'ISET'Com et obtenez des réponses utiles!")

# Display predefined questions in the sidebar
st.sidebar.header("Questions Prêtes à l'Emploi")
for question in questions:
    if st.sidebar.button(question):
        # Add question to chat history
        st.session_state.chat_history.append({"role": "user", "parts": [question]})

        # Generate chatbot response using Gemini
        prompt = []
        for message in st.session_state.chat_history:
            for part in message["parts"]:
                if isinstance(part, str):
                    prompt.append(f"{message['role']}: {part}")
                elif isinstance(part, genai.File):
                    prompt.append(f"{message['role']}: <file:{part.uri}>")
        prompt = "\n".join(prompt)
        response = model.generate_content(prompt)

        # Add chatbot response to chat history
        st.session_state.chat_history.append({"role": "assistant", "parts": [response.text]})

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        with st.chat_message("user"):
            for part in message["parts"]:
                if isinstance(part, str):
                    st.write(part)
                elif isinstance(part, genai.File):
                    st.write(f"File: {part.display_name}")
    else:
        with st.chat_message("assistant"):
            for part in message["parts"]:
                if isinstance(part, str):
                    st.write(part)

# User input
user_input = st.chat_input("Ou posez votre propre question:")
if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "parts": [user_input]})

    # Generate chatbot response using Gemini
    prompt = []
    for message in st.session_state.chat_history:
        for part in message["parts"]:
            if isinstance(part, str):
                prompt.append(f"{message['role']}: {part}")
            elif isinstance(part, genai.File):
                prompt.append(f"{message['role']}: <file:{part.uri}>")
    prompt = "\n".join(prompt)
    response = model.generate_content(prompt)

    # Add chatbot response to chat history
    st.session_state.chat_history.append({"role": "assistant", "parts": [response.text]})

    # Display chatbot response
    with st.chat_message("assistant"):
        st.write(response.text)

