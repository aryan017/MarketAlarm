from fastapi import FastAPI, WebSocket
import redis
from pymongo import MongoClient
import requests

app = FastAPI()

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["stock_alerts"]
alerts_collection = db["alerts"]

active_connections = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        active_connections.remove(websocket)

async def notify_users(stock, price):
    """Send WebSocket alerts to users"""
    for conn in active_connections:
        await conn.send_text(f"Stock {stock} crossed target price: {price}")
