from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from utils.logger import log_info, log_error
import os

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0
)
memory = ConversationBufferMemory()

conversation = ConversationChain(
    llm=llm,
    memory=memory
)

def risk_agent(query):
    log_info(f"Risk Agent Query: {query}")

    try:
        prompt = f"""
        You are a financial advisor.

        If user gives incomplete info, ASK for:
        - Age
        - Monthly income
        - Risk appetite (Low/Medium/High)

        DO NOT give final answer until you get this info.

        If all info is available, then:
        - Suggest investment plan
        - Give percentage allocation
        - Mention risks

        Conversation:
        {query}
        """

        response = conversation.predict(input=query)

        return response

    except Exception as e:
        log_error(f"Risk agent error: {str(e)}")
        return "⚠️ Risk analysis failed"