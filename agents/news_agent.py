from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI()



def news_agent(query):
    response = llm.invoke(f"Summarize financial news: {query}")
    return response.content