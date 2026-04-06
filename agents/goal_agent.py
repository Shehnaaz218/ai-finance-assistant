from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI()

def goal_agent(query):
    response = llm.invoke(f"Help plan financial goals: {query}")
    return response.content