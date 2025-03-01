from fastapi import APIRouter
from pymongo import MongoClient
import asyncio
import os
from app.models import Alert
from dotenv import load_dotenv
from app.upstox_client import UpstoxClient
from app.websocket import broadcast_message

load_dotenv()
router = APIRouter()
client = MongoClient("mongodb://localhost:27017/")
db = client["stock_alerts"]
alerts_collection = db["alerts"]

upstox_client = UpstoxClient(api_key=os.getenv("UPSTOX_API_KEY"), access_token=os.getenv("UPSTOX_ACCESS_TOKEN"))


@router.post("/alert")
async def create_alert(alert: Alert):
    # Save the alert to MongoDB.
    alerts_collection.insert_one(alert.dict())

    # Start monitoring for this alert.
    asyncio.create_task(
        upstox_client.monitor_stock(alert.symbol, alert.target_price, broadcast_message)
    )

    return {"status": "Alert created"}  # ✅ Removed extra comma

