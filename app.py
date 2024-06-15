from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

# Configure the generative AI model with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the generative model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def getGenAIResponse(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize the Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM APP", divider='rainbow')

# Add custom CSS to fix the input form at the bottom and style the chat history
st.markdown("""
    <style>
    .chat-input {
        position: fixed;
        bottom: 0;
        width: 100%;
        background: white;
        padding: 10px;
        box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
        z-index: 1000;
    }
    .chat-history {
        padding-bottom: 80px;  /* Adjust padding to ensure chat history is visible above the input */
        padding-top: 50px;
        overflow-y: auto;
        height: calc(100vh - 130px);
    }
    .ai-response {
        border-radius: 10px;
        padding: 10px;
        margin-top: 10px;
        white-space: pre-wrap;
    }
    .user-message {
        border-radius: 10px;
        padding: 10px;
        margin-top: 10px;
        white-space: pre-wrap;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state if chat history does not exist
if 'chatHistory' not in st.session_state:
    st.session_state['chatHistory'] = []

# Display the chat history
chat_history_container = st.container()
with chat_history_container:
    st.subheader("Chat History")
    for role, text in st.session_state['chatHistory']:
        if role == "AI":
            st.markdown(f'<div class="ai-response"><b>{role}</b>: {text}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="user-message"><b>{role}</b>: {text}</div>', unsafe_allow_html=True)

# Create a form for user input at the bottom
input_form_container = st.container()
with input_form_container:
    with st.form(key='my_form', clear_on_submit=True):
        input_text = st.text_input("Input:", key="input", label_visibility="collapsed")
        submit_button = st.form_submit_button(label='Ask question', use_container_width=True)

# Process the user input when the form is submitted
if submit_button and input_text:
    response = getGenAIResponse(input_text)
    st.session_state['chatHistory'].append(("You", input_text))
    temp_response = ''
    for chunk in response:
        temp_response += chunk.text
    st.session_state['chatHistory'].append(("AI", temp_response))
    
    # Rerun the script to refresh the chat history display
    st.rerun()
