import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

st.title("Chatbot")
with st.sidebar:
    st.title("User account")
    user_email = st.text_input('Email: ')
    user_pass = st.text_input('Password: ', type='password')
    if not (user_email and user_pass):
        st.warning('Please enter your account')
    else:
        st.success('Log in success')

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "How may I help you ?"}]
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


def generate_respond(prompt_input, email, password):
    sign = Login(email, password)
    cookies = sign.login()
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot.chat(prompt_input)


if prompt := st.chat_input(disabled=not (user_email and user_pass)):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("users"):
        st.write(prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            response = generate_respond(prompt, user_email, user_pass)
            st.write(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
