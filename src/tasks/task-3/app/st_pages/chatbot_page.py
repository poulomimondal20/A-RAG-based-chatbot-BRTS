import warnings
import pandas as pd
import streamlit as st
import plotly.express as px

def main(chatbot):
    # if "messages" not in st.session_state:
    #     st.session_state.messages = []

    # for message in st.session_state.messages:
    #     with chatbot.chat_message(message["role"]):
    #         st.write(f"<p class='poppins-light'>{message["content"]}</p>", unsafe_allow_html=True)

    # if prompt := chatbot.chat_input("What's up?"):
    #     with chatbot.chat_message("user"):
    #         st.write(f"<p class='poppins-light'>{prompt}</p>", unsafe_allow_html=True)
    #     st.session_state.messages.append({"role": "user", "content": prompt})
    chatbot.write("""<h3><i class="fa-regular fa-message"></i>&nbsp;&nbsp;Chatbot</h3>""", unsafe_allow_html=True)

if __name__ == '__main__':
    main(st)