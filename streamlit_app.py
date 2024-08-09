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
    "max_output_tokens": 512,  # Adjust as needed
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini."""
    print(f"Path: {path}")  # Added for debugging
    with open(path, "rb") as f:
        file = genai.upload_file(f, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def wait_for_files_active(files):
    """Waits for the given files to be active."""
    print("Waiting for file processing...")
    for file in files:
        while file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            file = genai.get_file(file.name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")
    print("...all files ready")
    print()

# Specify the paths to your local files
file_paths = [
    r"data/Plan_d_etude_RST_semestres_4_5_et_6_.pdf",
    r"data/Plan_d_etude_SR_semestres_4_5_et_6_.pdf",
    r"data/Plan_d_etude_STIC_semestres_1_2_et_3_.pdf",
    r"data/Plan_d_etude_MASTER.pdf",
    r"data/Plan_d_etude_GTIC.pdf",
    r"data/last-scores.jpg"
    # Add other file paths as needed
]

# Upload files to Gemini
files = [upload_to_gemini(path, mime_type="application/pdf") for path in file_paths]

# Wait for files to be active
wait_for_files_active(files)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "user",
            "parts": [
                "Vous etes un chat bot de guide des nouveaux etudiants , faq , ... ",
                *files,  # Include all uploaded files
            ],
        },
        # ... (rest of the initial chat history)
    ]

# --- Streamlit App UI ---
st.title("🎓 University Guide Chatbot 🤖")
st.write("Ask questions about your institute and get helpful answers!")

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
user_input = st.chat_input("Ask a question:")
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
