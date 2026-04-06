import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


import streamlit as st
from workflow.router import route_query

st.set_page_config(page_title="AI Finance Assistant", layout="centered")

st.title("💰 AI Finance Assistant")

st.write("Ask anything about finance, stocks, tax, or goals!")

# Input
user_input = st.text_input("Enter your question:")

# Button
if st.button("Ask AI"):
    if user_input:
        response = route_query(user_input)
        st.write("### 🤖 AI Response:")
        st.write(response)
    else:
        st.warning("Please enter a question")