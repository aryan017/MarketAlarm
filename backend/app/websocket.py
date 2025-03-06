from app.main import clients

async def broadcast_message(message: str):
    for client in clients:
        try:
            await client.send_text(message)
        except Exception as e:
            print("Error sending message:", e)