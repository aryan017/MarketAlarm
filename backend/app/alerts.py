# app/alerts.py
from fastapi import APIRouter
from pymongo import MongoClient
import asyncio
from app.models import Alert
from app.upstox_client import upstox_client  # Ensure proper import based on your project structure
from app.websocket import broadcast_message

router = APIRouter()
client = MongoClient("mongodb://localhost:27017/")
db = client["stock_alerts"]
alerts_collection = db["alerts"]

@router.post("/alert")
async def create_alert(alert: Alert):
    # Save the alert to MongoDB.
    alerts_collection.insert_one(alert.dict())
    # Start monitoring for this alert.
    asyncio.create_task(
        upstox_client.monitor_stock(alert.symbol, alert.target_price, broadcast_message)
    )
    return {"status": "Alert created"}
