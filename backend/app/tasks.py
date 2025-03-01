import asyncio
from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
from app.upstox_client import UpstoxClient
import os
from app.websocket import broadcast_message  

load_dotenv()
app = FastAPI()
client = MongoClient("mongodb://localhost:27017/")
db = client["stock_alerts"]
alerts_collection = db["alerts"]

upstox_client = UpstoxClient(api_key=os.getenv("UPSTOX_API_KEY"), access_token=os.getenv("UPSTOX_ACCESS_TOKEN"))

@app.on_event("startup")
async def start_stock_monitor():

    existing_alerts = alerts_collection.find()
    
    for alert in existing_alerts:
        asyncio.create_task(
            upstox_client.monitor_stock(alert["symbol"], alert["target_price"], broadcast_message)
        )
