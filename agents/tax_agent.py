import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load API key
load_dotenv()

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0
)

# Tax Agent Function
def tax_agent(query):
    response = llm.invoke(f"Explain this tax-related query in simple terms for a beginner: {query}")
    return response.content