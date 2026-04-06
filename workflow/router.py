from agents.finance_agent import finance_agent
from agents.portfolio_agent import portfolio_agent
from agents.market_agent import market_agent
from agents.goal_agent import goal_agent
from agents.tax_agent import tax_agent
from agents.news_agent import news_agent

def route_query(query):
    query = query.lower()

    if "portfolio" in query:
        return portfolio_agent(query)
    elif "market" in query or "stock" in query:
        return market_agent(query)
    elif "goal" in query or "plan" in query:
        return goal_agent(query)
    elif "tax" in query:
        return tax_agent(query)
    elif "news" in query:
        return news_agent(query)
    else:
        return finance_agent(query)