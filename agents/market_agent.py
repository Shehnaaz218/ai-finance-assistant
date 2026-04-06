import os
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
from api.stock_api import get_stock_price

load_dotenv()

llm = llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def market_agent(query):
    query = query.lower()

    # Simple stock detection
    if "price" in query:
        words = query.split()
        symbol = words[-1].upper()   # last word as stock symbol
        return get_stock_price(symbol)

    response = llm.invoke(f"Give market insights: {query}")
    return response.content