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

# --- Tab Management ---
tabs = ["Guide Chatbot", "Gallery"]  # Add more tabs as needed
selected_tab = st.sidebar.tabs(tabs)

# --- Content and Sidebar based on Tab ---
if selected_tab == "Guide Chatbot":
    st.title("🎓 Iset'Com Guide Chatbot 🤖")
    st.write("Posez des questions sur l'ISET'Com et obtenez des réponses utiles!")
    # Display Social media links in the sidebar
    st.sidebar.markdown(
        """
        [![Facebook](https://img.shields.io/badge/-Facebook-1877F2?logo=facebook&logoColor=white)](https://www.facebook.com/ISETCom)
        [![Iset'Comian'S](https://img.shields.io/badge/FB_GROUP-Iset_ComianS-blue)](https://www.facebook.com/groups/377145616641546) 
        [![LinkedIn](https://img.shields.io/badge/-LinkedIn-0077B5?logo=linkedin&logoColor=white)](https://tn.linkedin.com/school/iset-com/)
        [![Website](https://img.shields.io/badge/-Website-0077B5?logo=website&logoColor=white)](https://isetcom.tn/)
        
        """
    )

    # display university image
    st.sidebar.image("https://scontent.ftun10-2.fna.fbcdn.net/v/t1.6435-9/117945334_1707831949375490_3804404197353496189_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=25d718&_nc_ohc=YtNKkPn_B6wQ7kNvgGrq6fC&_nc_ht=scontent.ftun10-2.fna&oh=00_AYCggODOaRxAkp0PIzFA-m-YF2GdA8LwDfA6gycmB2-tjw&oe=66DEFF72")

    # Sidebar with predefined questions
    st.sidebar.header("Questions Prêtes à l'Emploi")
    for question in questions:
        if st.sidebar.button(question):
            user_input = question
            # Generate chatbot response
            response = model.generate_content(f"user: {user_input}")
            # Display response
            with st.chat_message("assistant"):
                st.write(response.text)

    # User input
    user_input = st.chat_input("Ou posez votre propre question:")
    if user_input:
        # Generate chatbot response
        response = model.generate_content(f"user: {user_input}")
        # Display response
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