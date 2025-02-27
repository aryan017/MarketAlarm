from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for connected WebSocket clients.
clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Process incoming messages if necessary.
            print("Received:", data)
    except WebSocketDisconnect:
        clients.remove(websocket)

async def broadcast_message(message: str):
    for client in clients:
        try:
            await client.send_text(message)
        except Exception as e:
            print("Error sending message:", e)
