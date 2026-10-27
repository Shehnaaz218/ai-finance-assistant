
import sys
import os
import time
import uuid

import streamlit as st
from dotenv import load_dotenv

# --------------------------------------------------
# ENVIRONMENT AND IMPORTS
# --------------------------------------------------

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

load_dotenv(os.path.join(BASE_DIR, ".env"))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from workflow.router import route_query
from evaluation.evaluator import evaluate_response
from database import (
    initialize_database,
    create_chat,
    list_chats,
    load_messages,
    save_message,
    log_query,
)

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="FINNIE AI",
    layout="wide"
)

# Initialize PostgreSQL tables.
try:
    initialize_database()
except Exception:
    st.error(
        "Unable to connect to the database. "
        "Please check DATABASE_URL in your environment settings."
    )
    st.stop()

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.title("💬 Chats")

    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.current_chat = None
        st.rerun()

    st.markdown("---")
    st.subheader("Previous Chats")

    try:
        previous_chats = list_chats()

        if not previous_chats:
            st.caption("No previous chats yet.")

        for chat_id, title in previous_chats:
            if st.button(
                title,
                key=f"chat_{chat_id}",
                use_container_width=True
            ):
                st.session_state.current_chat = chat_id
                st.session_state.messages = load_messages(chat_id)
                st.rerun()

    except Exception:
        st.error("Unable to load previous chats.")

    # --------------------------------------------------
    # RISK PROFILE FORM
    # --------------------------------------------------

    st.markdown("---")
    st.subheader("📊 Risk Profile")

    with st.form("risk_form"):
        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=25
        )

        income = st.number_input(
            "Monthly Income (₹)",
            min_value=0,
            value=0
        )

        risk_level = st.selectbox(
            "Risk Appetite",
            ["Low", "Medium", "High"]
        )

        submit = st.form_submit_button("Analyze Risk")

    if submit:
        risk_query = f"""
User Profile:
Age: {age}
Monthly Income: ₹{income}
Risk Level: {risk_level}

Suggest an investment plan for ₹1 lakh.
"""

        try:
            with st.spinner("Analyzing your risk profile..."):
                response = route_query(risk_query)
                evaluation = evaluate_response(
                    risk_query, response
                )

            # Create a separate persistent conversation.
            risk_chat_id = str(uuid.uuid4())

            create_chat(
                risk_chat_id,
                f"Risk Profile - {risk_level}"
            )

            save_message(
                risk_chat_id, "user", risk_query
            )
            log_query(risk_chat_id, risk_query)
            save_message(
                risk_chat_id, "assistant", response
            )

            st.session_state.current_chat = risk_chat_id
            st.session_state.messages = load_messages(
                risk_chat_id
            )

            st.success("Risk analysis saved to chat history.")

            
            st.subheader("📊 Evaluation Metrics")
            st.json(evaluation)

        except Exception:
            st.error(
                "Risk analysis failed. "
                "Please check the application logs."
            )

# --------------------------------------------------
# MAIN UI
# --------------------------------------------------

st.title("💰 FINNIE AI")
st.caption(
    "Ask anything about finance, tax, stocks & investments 📊"
)
st.markdown("---")

# --------------------------------------------------
# DISPLAY CURRENT CHAT
# --------------------------------------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

user_input = st.chat_input(
    "Ask your finance question..."
)

if user_input:
    try:
        # Create a new conversation if needed.
        if st.session_state.current_chat is None:
            chat_id = str(uuid.uuid4())

            # Use the first query as the conversation title.
            title = " ".join(user_input.split())[:40]
            title = title or "New Chat"

            create_chat(chat_id, title)
            st.session_state.current_chat = chat_id

        chat_id = st.session_state.current_chat

        # Save and display the user message.
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        save_message(chat_id, "user", user_input)
        log_query(chat_id, user_input)

        with st.chat_message("user"):
            st.markdown(user_input)

        # Get AI response using the existing workflow.
        with st.spinner("Thinking..."):
            response = route_query(
            user_input,
            chat_history=st.session_state.messages[:-1]
        )

        # Evaluate the AI response.
        evaluation = evaluate_response(
            user_input, response
        )

        # Display response with typing effect.
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_text = ""

            for word in response.split():
                full_text += word + " "
                placeholder.markdown(full_text)
                time.sleep(0.01)

            with st.expander("📊 Evaluation Metrics"):
                st.json(evaluation)

        # Persist the assistant response.
        save_message(chat_id, "assistant", response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        st.rerun()

    except Exception as e:
        st.error(f"Query failed: {type(e).__name__}: {e}")
        st.exception(e)
