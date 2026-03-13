def detect_intent(query: str):
    query = query.lower().strip()

    greetings = ["hello", "hi", "hey", "good morning", "good evening"]

    for g in greetings:
        if query == g:
            return "greeting"

    return "legal_query"