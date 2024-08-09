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
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

def wait_for_files_active(files):
  """Waits for the given files to be active.

  Some files uploaded to the Gemini API need to be processed before they can be
  used as prompt inputs. The status can be seen by querying the file's "state"
  field.

  This implementation uses a simple blocking polling loop. Production code
  should probably employ a more sophisticated approach.
  """
  print("Waiting for file processing...")
  for name in (file.name for file in files):
    file = genai.get_file(name)
    while file.state.name == "PROCESSING":
      print(".", end="", flush=True)
      time.sleep(10)
      file = genai.get_file(name)
    if file.state.name != "ACTIVE":
      raise Exception(f"File {file.name} failed to process")
  print("...all files ready")
  print()


# TODO Make these files available on the local file system
# You may need to update the file paths
files = [
  upload_to_gemini("Plan_d_etude_RST_semestres_4_5_et_6_.pdf", mime_type="application/pdf"),
  upload_to_gemini("Plan_d_etude_SR_semestres_4_5_et_6_.pdf", mime_type="application/pdf"),
  upload_to_gemini("Plan_d_etude_STIC_semestres_1_2_et_3_.pdf", mime_type="application/pdf"),
  upload_to_gemini("Plan_d_etude_MASTER.pdf", mime_type="application/pdf"),
  upload_to_gemini("Plan_d_etude_GTIC.pdf", mime_type="application/pdf"),
  upload_to_gemini("Unknown File", mime_type="application/octet-stream"),
]

# Some files have a processing delay. Wait for them to be ready.
wait_for_files_active(files)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
    {
      "role": "user",
      "parts": [
        "Vous etes un chat bot de guide des nouveaux etudiants , faq , ... ",
        files[0],
        files[1],
        files[2],
        files[3],
        files[4],
      ],
    },
    {
      "role": "model",
      "parts": [
        "Bonjour ! Je suis un chatbot conçu pour aider les nouveaux étudiants à se familiariser avec leur parcours universitaire.\n\nD'après les documents que vous avez fournis, je vois que vous êtes Salima et que vous allez commencer une Licence en Réseaux et Systèmes des Télécommunications, n'est-ce pas ? Félicitations pour votre admission ! \n\nJe peux vous fournir des informations sur :\n\n* **Les unités d'enseignement (UE) et les éléments constitutifs (EE) de chaque semestre :**  Je peux vous détailler les cours qui vous seront proposés, leurs coefficients et le volume horaire de chacun. Par exemple, au semestre 4, l'UE \"Systèmes d'accès télécoms\" (code 576102410) comprend deux EEs : \"Les réseaux d'accès sans fil\" et \"Atelier réseaux d'accès\".\n* **Les différents types d'enseignements :** Cours magistraux (Cours), Travaux Dirigés (TD), Travaux Pratiques (TP) ...\n* **Les modalités d'évaluation :** Contrôle continu (CC) \n* **Les abréviations utilisées :**  Nat (Nature de l'UE : Fondamentale, Transversale...), Cr (crédits), Coef (coefficient), Rg (régime d'examen).\n\n\nN'hésitez pas à me poser des questions plus précises. Par exemple :\n\n* \"Quels sont les cours que j'aurai au semestre 5 ?\"\n* \"Quel est le coefficient de l'UE 'Objets connectés et IoT' ?\"\n* \"Que signifie 'C.Int' dans le tableau ?\"\n\nPlus vous êtes précis dans vos questions, plus je pourrai vous fournir des réponses utiles et pertinentes. \n\nJ'ai également accès aux informations concernant la Licence en Sécurité des Réseaux et la Licence Tronc Commun. Si vous avez des questions à propos de ces parcours, n'hésitez pas à me les poser.\n\nJe suis là pour vous aider à démarrer votre parcours universitaire du bon pied !\n",
      ],
    },
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
                    st.write(f"File: {part.display_name}")  # Display file name
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
