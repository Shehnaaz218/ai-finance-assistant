from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI()

def finance_agent(query):
    response = llm.invoke(f"Explain: {query}")
    return response.content