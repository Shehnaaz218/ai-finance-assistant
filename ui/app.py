import sys
import os
import json
import time
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from the project root .env file
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))



# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from workflow.router import route_query
from evaluation.evaluator import evaluate_response

# -----------------------------
# STORAGE
# -----------------------------
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

CHAT_DIR = os.path.join(BASE_DIR, "chats")
os.makedirs(CHAT_DIR, exist_ok=True)

def get_chat_files():
    return sorted(
        [
            filename
            for filename in os.listdir(CHAT_DIR)
            if filename.endswith(".json")
        ],
        key=lambda filename: os.path.getmtime(
            os.path.join(CHAT_DIR, filename)
        ),
        reverse=True
    )

def load_chat(filename):
    with open(os.path.join(CHAT_DIR, filename), "r") as f:
        return json.load(f)

def save_chat(filename, messages):
    with open(os.path.join(CHAT_DIR, filename), "w") as f:
        json.dump(messages, f)

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="FINNIE AI ", layout="wide")

# -----------------------------
# SESSION STATE
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.title("💬 Chats")

    if st.button("➕ New Chat"):
        st.session_state.messages = []
        st.session_state.current_chat = None

    st.markdown("---")
    st.subheader("Previous Chats")

    for chat in get_chat_files():
        display_name = chat.replace(".json", "").replace("_", " ")

        if st.button(display_name):
            st.session_state.current_chat = chat
            st.session_state.messages = load_chat(chat)

    # -----------------------------
    # RISK FORM
    # -----------------------------
    st.markdown("---")
    st.subheader("📊 Risk Profile")

    with st.form("risk_form"):
        age = st.number_input("Age", min_value=18, max_value=100)
        income = st.number_input("Monthly Income (₹)", min_value=0)
        risk_level = st.selectbox("Risk Appetite", ["Low", "Medium", "High"])

        submit = st.form_submit_button("Analyze Risk")

    if submit:
        risk_query = f"""
        User Profile:
        Age: {age}
        Income: {income}
        Risk Level: {risk_level}

        Suggest investment plan for 1 lakh.
        """

        response = route_query(risk_query)
        evaluation = evaluate_response(risk_query, response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        with st.chat_message("assistant"):
            st.markdown(response)

            with st.expander("📊 Evaluation Metrics"):
                st.json(evaluation)

# -----------------------------
# MAIN UI
# -----------------------------
st.title("💰 FINNIE AI")
st.caption("Ask anything about finance, tax, stocks & investments 📊")
st.markdown("---")

# -----------------------------
# DISPLAY CHAT
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# USER INPUT
# -----------------------------
user_input = st.chat_input("Ask your finance question...")

if user_input:

    # -----------------------------
    # CREATE CHAT NAME
    # -----------------------------
    if st.session_state.current_chat is None:
        safe_name = "".join(c for c in user_input if c.isalnum() or c == " ")[:30]
        safe_name = safe_name.strip().replace(" ", "_")

        if not safe_name:
            safe_name = "Chat"

        st.session_state.current_chat = safe_name + ".json"

    # -----------------------------
    # STORE USER MESSAGE
    # -----------------------------
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # -----------------------------
    # GET RESPONSE
    # -----------------------------
    response = route_query(user_input)

    # -----------------------------
    # EVALUATION
    # -----------------------------
    evaluation = evaluate_response(user_input, response)

    # -----------------------------
    # DISPLAY RESPONSE (typing effect)
    # -----------------------------
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""

        for word in response.split():
            full_text += word + " "
            placeholder.markdown(full_text)
            time.sleep(0.01)

        with st.expander("📊 Evaluation Metrics"):
            st.json(evaluation)

    # -----------------------------
    # STORE RESPONSE
    # -----------------------------
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    # -----------------------------
    # SAVE CHAT
    # -----------------------------
    save_chat(st.session_state.current_chat, st.session_state.messages)
    