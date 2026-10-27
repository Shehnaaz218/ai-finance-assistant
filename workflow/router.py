
from agents.finance_agent import finance_agent
from agents.portfolio_agent import portfolio_agent
from agents.market_agent import market_agent
from agents.goal_agent import goal_agent
from agents.tax_agent import tax_agent
from agents.news_agent import news_agent

FINANCE_KEYWORDS = {
    "finance", "financial", "money", "budget", "saving", "savings",
    "invest", "investment", "investments", "stock", "stocks", "market",
    "portfolio", "mutual fund", "mutual funds", "fixed deposit",
    "fd", "interest", "loan", "loans", "credit", "debt", "tax",
    "income", "expense", "expenses", "salary", "bank", "banking",
    "insurance", "retirement", "sip", "equity", "dividend",
    "profit", "loss", "inflation", "emi", "financial goal",
    "goal", "plan", "rupee", "rupees", "inr", "₹",
    "nifty", "sensex", "share", "shares", "gst", "itr"
}

GUARDRAIL_MESSAGE = "⚠️ Please ask finance-related questions only."


def is_finance_query(query):
    text = query.lower().strip()

    if not text:
        return False

    return any(keyword in text for keyword in FINANCE_KEYWORDS)


def route_query(query, chat_history=None):
    if not is_finance_query(query):
        return GUARDRAIL_MESSAGE

    normalized_query = query.lower()

    if "portfolio" in normalized_query:
        return portfolio_agent(query)
    elif "market" in normalized_query or "stock" in normalized_query:
        return market_agent(query)
    elif "goal" in normalized_query or "plan" in normalized_query:
        return goal_agent(query)
    elif "tax" in normalized_query:
        return tax_agent(query)
    elif "news" in normalized_query:
        return news_agent(query)
    else:
        return finance_agent(query, chat_history=chat_history)

