import asyncio
from fastapi import FastAPI
from app.upstox_client import UpstoxClient
from app.websocket import broadcast_message  # if defined in a separate module

upstox_client = UpstoxClient(api_key="YOUR_API_KEY", access_token="YOUR_ACCESS_TOKEN")

@app.on_event("startup")
async def start_stock_monitor():
    # Example: Monitor stock "AAPL" with target price 150.0.
    asyncio.create_task(
        upstox_client.monitor_stock("AAPL", 150.0, broadcast_message)
    )
