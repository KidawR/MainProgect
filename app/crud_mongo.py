from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["cafe_mongo"]

reviews = db["reviews"]
logs = db["logs"]

# ===== Reviews =====
def add_review(customer_id, branch_id, rating, comment, sentiment):
    if not (1 <= sentiment <= 5):
        raise ValueError("sentiment должен быть числом от 1 до 5")
    reviews.insert_one({
        "customer_id": customer_id,
        "branch_id": branch_id,
        "rating": rating,
        "comment": comment,
        "sentiment": sentiment,
        "created_at": datetime.utcnow()
    })

def get_reviews(branch_id=None):
    query = {}
    if branch_id:
        query["branch_id"] = branch_id
    return list(reviews.find(query, {"_id": 0}))

# ===== Logs =====
def log_action(user_id, action, details=None):
    logs.insert_one({
        "user_id": user_id,
        "action": action,
        "details": details,
        "timestamp": datetime.utcnow()
    })
