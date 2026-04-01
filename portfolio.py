def create_plan(goal, risk):
    # Dummy investment plans using MPT-like logic
    plans = {
        "retirement": {"equities": 60, "bonds": 30, "cash": 10},
        "vacation": {"equities": 30, "bonds": 60, "cash": 10},
        "education": {"equities": 40, "bonds": 50, "cash": 10}
    }
    risk_map = {"low": 0.7, "medium": 1.0, "high": 1.3}
    plan = plans.get(goal, plans["retirement"])
    # Apply risk weighting (in reality, much more complex)
    for asset in plan:
        plan[asset] *= risk_map.get(risk, 1)
    return plan
