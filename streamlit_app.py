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

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

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
