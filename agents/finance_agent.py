import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def finance_agent(query):
    response = llm.invoke(f"Explain: {query}")
    return response.content