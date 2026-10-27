import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0
)

def portfolio_agent(query):
    response = llm.invoke(f"Analyze this portfolio or investment query: {query}")
    return response.content