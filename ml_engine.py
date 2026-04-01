import spacy
nlp = spacy.load("en_core_web_sm")

CATEGORIES = {
    "Starbucks": "Coffee",
    "Amazon": "Shopping",
    "Uber": "Transport",
    # Add more mappings as needed
}

def categorize(transactions):
    result = []
    for txn in transactions:
        desc = txn.get("description", "")
        cat = CATEGORIES.get(desc, "Miscellaneous")
        result.append({"id": txn.get("id"), "category": cat})
    return result
