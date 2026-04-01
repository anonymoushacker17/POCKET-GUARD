def set_spending_caps(budget):
    # Set category-specific caps from user budget
    caps = {cat: budget[cat] * 0.90 for cat in budget}
    return caps

def perform_auto_save(income, percent):
    # Move percent of income to savings
    amount_saved = income * percent / 100.0
    # In production: initiate API call to bank for transfer
    return amount_saved
