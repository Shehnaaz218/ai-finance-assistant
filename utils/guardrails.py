def check_input(query):
    query_lower = query.lower()

    # Block non-finance topics
    blocked_topics = ["football", "movie", "cricket", "actor", "politics"]

    for word in blocked_topics:
        if word in query_lower:
            return False, "⚠️ Please ask finance-related questions only."

    return True, query


def check_output(response):
    # Basic safety check
    if "guaranteed profit" in response.lower():
        return "⚠️ Investment involves risk. No returns are guaranteed."

    return response