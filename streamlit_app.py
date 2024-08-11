import streamlit as st
import os
import google.generativeai as genai

# Set page config
st.set_page_config(page_title="Iset'Com Guide Chatbot", page_icon="🎓", layout="wide")

# Get API key
api_key = os.getenv("API")
if api_key is None:
    st.error("Error: API environment variable is not set.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)

# Create the model
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 4096,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Reponds en francais , tunisien"
)

# Predefined questions
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
    "Quels sont les scores des derniers étudiants admis à l'ISET'Com?"
]

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Start with an empty list

# --- Tab Management ---
tabs = ["Guide Chatbot", "Gallery"]
selected_tab = st.tabs(tabs)

# --- Content and Sidebar based on Tab ---
if selected_tab == "Guide Chatbot":
    st.title("🎓 Iset'Com Guide Chatbot 🤖")
    st.write("Posez des questions sur l'ISET'Com et obtenez des réponses utiles!")

    # Sidebar with predefined questions
    st.sidebar.header("Questions Prêtes à l'Emploi")
    for question in questions:
        if st.sidebar.button(question):
            # Add question to chat history
            st.session_state.chat_history.append({"role": "user", "parts": [question]})

            # Generate chatbot response
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

        # Generate chatbot response
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


elif selected_tab == "Gallery":
    st.title("🖼️ Iset'Com Gallery")
    st.write("Découvrez la vie étudiante à l'ISET'Com en images!")

    # Add gallery content here (e.g., using st.image)
    # ...

    # Update sidebar for the Gallery tab
    st.sidebar.header("Gallery Options")
    # Add options like filtering images by category, etc.
    # ...

# --- Add more tabs and content as needed ---