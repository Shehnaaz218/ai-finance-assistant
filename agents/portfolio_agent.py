from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI()

def portfolio_agent(query):
    response = llm.invoke(f"Analyze this portfolio or investment query: {query}")
    return response.content