def classify_intent(query):
    query = query.lower()

    if any(w in query for w in ["destination", "place", "visit", "attraction", "city", "country"]):
        return "DESTINATIONS"
    if any(w in query for w in ["hotel", "stay", "accommodation", "resort", "booking"]):
        return "ACCOMMODATION"
    if any(w in query for w in ["flight", "bus", "train", "transport", "taxi", "travel time"]):
        return "TRANSPORT"
    if any(w in query for w in ["food", "restaurant", "cuisine", "eat", "dish"]):
        return "FOOD"

    return "GENERAL"
