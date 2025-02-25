import redis
import asyncio
from pymongo import MongoClient
from main import notify_users

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["stock_alerts"]
alerts_collection = db["alerts"]

async def check_alerts():
    """Check if any stock crossed user-defined price and send alerts"""
    while True:
        alerts = alerts_collection.find({})
        for alert in alerts:
            symbol = alert["symbol"]
            target_price = alert["target_price"]
            current_price = float(redis_client.get(symbol) or 0)
            
            if current_price >= target_price:
                await notify_users(symbol, current_price)
                alerts_collection.delete_one({"_id": alert["_id"]})  
    
        await asyncio.sleep(10)  

if __name__ == "__main__":
    asyncio.run(check_alerts())
