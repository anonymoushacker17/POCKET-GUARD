## (Root route will be defined after app and models are created)
from flask import Flask, request, jsonify
import traceback
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
import os
from pathlib import Path
import csv
from io import TextIOWrapper
import time
app = Flask(__name__)
# Configure CORS to allow frontend dev servers
CORS(
    app,
    resources={r"/api/*": {
        "origins": [
            "http://localhost:3000", "http://127.0.0.1:3000",
            "http://localhost:3001", "http://127.0.0.1:3001",
            "http://localhost:3002", "http://127.0.0.1:3002",
        ]
    }},
    supports_credentials=False,
)
home_instance_dir = Path.home() / ".pocketguard"
home_instance_dir.mkdir(parents=True, exist_ok=True)
db_file = os.environ.get("POCKETGUARD_DB", str(home_instance_dir / "pocketguard.db"))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# ----------------------------
# Models definition
# ----------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    token = db.Column(db.String, nullable=False)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String, nullable=False)
    cap = db.Column(db.Float, nullable=False)




@app.route('/api/link_account', methods=['POST', 'OPTIONS'])
@cross_origin(origins=[
    "http://localhost:3000", "http://127.0.0.1:3000",
    "http://localhost:3001", "http://127.0.0.1:3001",
    "http://localhost:3002", "http://127.0.0.1:3002",
], allow_headers=["Content-Type"], methods=["POST", "OPTIONS"])
def link_account():
    if request.method == 'OPTIONS':
        # Preflight request
        return ('', 204)
    try:
        data = request.json
        print("[DEBUG] /api/link_account received:", data, flush=True)
        username = data.get("credentials", {}).get("username")
        if not username:
            print("[ERROR] Missing username", flush=True)
            return jsonify({"success": False, "message": "Missing username"}), 400

        # Simulated token generation
        token = "token_" + username

        # Check if user exists, else create
        user = User.query.filter_by(username=username).first()
        if user:
            user.token = token
        else:
            user = User(username=username, token=token)
            db.session.add(user)
        db.session.commit()

        print(f"[DEBUG] Linked user: {username}, token: {token}", flush=True)
        return jsonify({"success": True, "token": token})
    except Exception as e:
        print(f"[ERROR] Exception in /api/link_account: {e}", flush=True)
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/transactions', methods=['POST'])
def categorize_transactions():
    data = request.json
    txns = data.get("transactions", [])
    

    categorized = []
    user = User.query.first()  # For demo, associate to first user
    if not user:
        return jsonify({"categorized": []})

    CATEGORY_MAP = {
        "Starbucks": "Coffee",
        "Amazon": "Shopping",
        "Uber": "Transport"
    }
    for txn in txns:
        desc = txn.get("description", "")
        category = CATEGORY_MAP.get(desc, "Miscellaneous")
        t = Transaction(user_id=user.id, description=desc, category=category)
        db.session.add(t)
        categorized.append({"id": txn.get("id"), "category": category})
    db.session.commit()
    return jsonify({"categorized": categorized})
@app.route('/api/budget', methods=['POST'])
def set_budget():
    data = request.json
    budget = data.get("budget", {})
    
    user = User.query.first()
    if not user:
        return jsonify({"caps": {}})
    
    caps = {}
    # Remove previous budgets for user
    Budget.query.filter_by(user_id=user.id).delete()
    for cat, amt in budget.items():
        cap_value = float(amt) * 0.90  # 10% saving cap
        caps[cat] = cap_value
        b = Budget(user_id=user.id, category=cat, cap=cap_value)
        db.session.add(b)
    db.session.commit()
    return jsonify({"caps": caps})

@app.route('/api/save', methods=['POST'])
def auto_save():
    data = request.json
    income = float(data.get("income", 0))
    percent = float(data.get("percent", 0))
    saved_amount = income * percent / 100.0
    # For demo, not persisting saving amounts yet
    return jsonify({"saved": saved_amount})

@app.route('/api/invest', methods=['POST'])
def invest():
    data = request.json
    goal = data.get("goal", "retirement")
    risk = data.get("risk", "medium")
    
    plans = {
        "retirement": {"equities": 42, "bonds": 21, "cash": 7},
        "vacation": {"equities": 30, "bonds": 60, "cash": 10},
        "education": {"equities": 40, "bonds": 50, "cash": 10}
    }
    risk_factor = {"low": 0.7, "medium": 1.0, "high": 1.3}
    plan = plans.get(goal, plans["retirement"])
    factor = risk_factor.get(risk, 1)
    adjusted_plan = {k: round(v * factor, 2) for k, v in plan.items()}
    return jsonify({"plan": adjusted_plan})

# #### New route for listing linked accounts
@app.route('/api/list_users', methods=['GET'])
def list_users():
    users = User.query.all()
    result = [{"username": u.username, "token": u.token} for u in users]

    return jsonify(result)

# Root route for health and endpoint listing
@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Pocket Guard Backend 🚀",
        "available_endpoints": [
            "/api/link_account",
            "/api/transactions",
            "/api/budget",
            "/api/save",
            "/api/invest",
            "/api/list_users"
        ]
    })

# Insights: summary totals by category and top merchants (last 30 days if dates present)
    # Removed insights and bills routes

# #### CSV Import for Transactions
    # Removed CSV import route

# #### Category mapping management
    # Removed category mapping management routes

# ----------------------------
# Run app
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
