import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))



def news_agent(query):
    response = llm.invoke(f"Summarize financial news: {query}")
    return response.content