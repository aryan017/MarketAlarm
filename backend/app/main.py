from fastapi import FastAPI, WebSocket, WebSocketDisconnect,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.alerts import router as alert_router
from app.websocket_manager import clients
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.auth import router as auth_router
from app.upstox_client import UpstoxClient
from app.websocket import broadcast_message
from jose import jwt, JWTError
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

upstox_client = UpstoxClient(api_key=os.getenv("UPSTOX_API_KEY"), access_token=os.getenv("UPSTOX_ACCESS_TOKEN"))


client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = client["stock_alerts"]
alerts_collection = db["alerts"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(alert_router)
app.include_router(auth_router)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        token = websocket.query_params.get("token")
        if not token:
            await websocket.close(code=1008)
            print("WebSocket closed: Missing token")
            return
        
        current_user = get_current_user(token)
        if not current_user:
            await websocket.close(code=1008)
            print("WebSocket closed: Invalid token")
            return
        
        user_email = current_user["email"]
        print(f"User connected: {user_email}")
        user_alerts = await alerts_collection.find({"user_contact": user_email}).to_list(length=100)
        print("User alerts:", user_alerts)
        for alert in user_alerts:
            print(alert)
            asyncio.create_task(
                upstox_client.monitor_stock(alert["symbol"], alert["target_price"], broadcast_message)
            )
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        clients.remove(websocket)
        print(f"User {user_email} disconnected.")

    except Exception as e:
        print(f"WebSocket Error: {e}")
        await websocket.close(code=1011)  

def get_current_user(token: str):
    """ Validate JWT and return user email """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"email": payload.get("sub")} 
    except JWTError:
        return None  