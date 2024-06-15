from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key= os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history= [])

def getGenAIResponse(question):
    response = chat.send_message(question, stream= True)
    return response

# Initialize the streamlit APP
st.set_page_config(page_title = "Q&A Demo")
st.header("Gemini LLM APP")

# Initilize session state if chat history is not exist
if 'chatHistory' not in st.session_state:
    st.session_state['chatHistory'] = []
    
input = st.text_input("Input :", key= "input")
submit = st.button("Ask question")

if submit and input:
    response = getGenAIResponse(input)
    st.session_state['chatHistory'].append(("You", input))
    st.subheader("Gemini :")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chatHistory'].append(("AI", chunk.text))
   
no_conversation = True        
if no_conversation == True:
    st.subheader("")
    no_conversation = False  
else:    
    st.subheader("The Chat History is")

for role, text in st.session_state['chatHistory']:
    st.write(f"{role}: {text}")
