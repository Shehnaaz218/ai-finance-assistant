import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0
)

def goal_agent(query):
    response = llm.invoke(f"Help plan financial goals: {query}")
    return response.content