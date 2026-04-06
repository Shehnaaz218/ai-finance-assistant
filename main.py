from workflow.router import route_query

while True:
    user_input = input("Ask your finance question: ")
    
    if user_input.lower() == "exit":
        break

    response = route_query(user_input)
    print("\nAI:", response)