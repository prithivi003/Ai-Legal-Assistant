def detect_intent(query: str):
    query = query.lower().strip()

    greetings = ["hello", "hi", "hey", "good morning", "good evening"]
    farewells = ["bye", "goodbye", "see you", "cya", "farewell"]

    for g in greetings:
        if query == g:
            return "greeting"
            
    for f in farewells:
        if query == f:
            return "farewell"

    return "legal_query"