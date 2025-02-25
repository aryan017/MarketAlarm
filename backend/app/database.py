from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["stock_alerts"]
alerts_collection = db["alerts"]

@app.post("/set_alert/")
def set_alert(symbol: str, target_price: float):
    """Save a user alert to MongoDB"""
    alerts_collection.insert_one({"symbol": symbol, "target_price": target_price})
    return {"message": f"Alert set for {symbol} at {target_price}"}
