
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0
)

def finance_agent(query, chat_history=None):
    messages = [
        SystemMessage(
            content=(
                "You are FINNIE AI, a helpful finance assistant. "
                "Answer finance-related questions clearly. "
                "Use the conversation history to understand follow-up "
                "questions and remember details shared earlier in this chat. "
                "Do not invent personal financial details."
            )
        )
    ]

    # Add previous messages from the current conversation
    if chat_history:
        for message in chat_history:
            role = message.get("role")
            content = message.get("content", "")

            if role == "user":
                messages.append(HumanMessage(content=content))
            elif role == "assistant":
                messages.append(AIMessage(content=content))

    # Add the current question
    messages.append(HumanMessage(content=query))

    response = llm.invoke(messages)
    return response.content
