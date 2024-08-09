import streamlit as st
import os
import google.generativeai as genai

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

# Predefined questions
questions = [
    "What are the most popular majors at this institute?",
    "What are the admission requirements?",
    "What are the available scholarships and financial aid options?",
    "What are the best student clubs and organizations to join?",
    "What are the on-campus housing options?",
    "How can I get involved in research opportunities?",
    "What are the career services and job placement resources?",
    "What are the best places to study on campus?",
    "What are some tips for succeeding in my first year?",
    "Where can I find information about tutoring and academic support?"
]

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
    {
      "role": "user",
      "parts": [
        files[5],
        "Bienvenue aux nouveaux étudiants de l'ISETCOM.\nNous sommes impatients de vous voir commencer cette nouvelle aventure académique avec nous.\n\nLes scores sont des derniers etudiant de differents bacs info , maths , sciences , technique qui ont ete acceptee a liset Com ",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Ah, je comprends mieux !  Il s'agit des scores du concours d'entrée à l'ISETCOM pour l'année 2024.  \n\nCe document montre les scores minimums requis pour être admis à l'ISETCOM, par filière du baccalauréat. \n\nPar exemple :\n\n* **Pour les étudiants ayant un baccalauréat en Sciences Expérimentales (علوم تجريبية) :**  Le score minimum pour être admis à la filière \"Sciences et Technologies de l'Information et de la Communication\" (code 10360) était de 144.38. \n* **Pour les étudiants ayant un baccalauréat en Mathématiques (رياضيات) :** Le score minimum pour être admis à la filière \"Sciences et Technologies de l'Information et de la Communication\" (code 10360) était de 156.47.\n\nCe document est très utile pour les nouveaux bacheliers qui souhaitent intégrer l'ISETCOM. Il leur permet de se situer et d'évaluer leurs chances d'admission.\n\nAvez-vous des questions sur ces scores d'admission ? Par exemple, souhaitez-vous savoir quel était le score minimum pour une filière en particulier ?  Ou bien voulez-vous connaître le score moyen d'admission pour une filière donnée ?\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "L'établissement en chiffres\n600\nEtudiants\n85%\nTaux de réussite\n26\nAns d'expérience\n3\nSpécialités\n\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Voici un excellent résumé de l'ISETCOM en quelques chiffres clés ! \n\nOn comprend vite pourquoi cet établissement est attractif :\n\n* **600 étudiants**: Une taille humaine qui favorise la proximité avec les enseignants et un environnement d'apprentissage convivial.\n* **85% de taux de réussite**: C'est un chiffre encourageant qui témoigne de la qualité de l'enseignement et de l'accompagnement des étudiants. \n* **26 ans d'expérience**:  L'ISETCOM a une longue histoire et une solide expertise dans la formation en Sciences et Technologies de l'Information et de la Communication.\n* **3 spécialités**:  L'établissement propose une offre de formation ciblée et pointue qui répond aux besoins du marché du travail.\n\n\nAvez-vous d'autres questions sur l'ISETCOM ?  Par exemple, aimeriez-vous en savoir plus sur les 3 spécialités proposées ?  Je suis là pour vous donner toutes les informations dont vous avez besoin.\n",
      ],
    },
  ]

# --- Streamlit App UI ---
st.title("🎓 University Guide Chatbot 🤖")
st.write("Ask questions about your institute and get helpful answers!")

# Display predefined questions
st.sidebar.header("Ready-Made Questions")
for question in questions:
    if st.sidebar.button(question):
        # Add question to chat history
        st.session_state.chat_history.append(f"input:{question}")

        # Generate chatbot response using Gemini
        prompt = st.session_state.chat_history.copy()
        prompt.append("output:")
        response = model.generate_content(prompt)

        # Add chatbot response to chat history
        st.session_state.chat_history.append(f"output:{response.text}")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message("assistant" if message.startswith("output:") else "user"):
        st.write(message.replace("input:", "").replace("output:", "").strip())

# User input (optional)
user_input = st.chat_input("Or ask your own question:")
if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append(f"input:{user_input}")

    # Generate chatbot response using Gemini
    prompt = st.session_state.chat_history.copy()
    prompt.append("output:")
    response = model.generate_content(prompt)

    # Add chatbot response to chat history
    st.session_state.chat_history.append(f"output:{response.text}")

    # Display chatbot response
    with st.chat_message("assistant"):
        st.write(response.text)
