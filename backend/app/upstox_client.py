import requests
import asyncio
import os

class UpstoxClient:
    def __init__(self, api_key: str, access_token: str):
        self.api_key = api_key or os.getenv("UPSTOX_API_KEY")
        self.access_token = access_token or os.getenv("UPSTOX_ACCESS_TOKEN")

    def get_stock_price(self, symbol: str) -> float:
        # Example API endpoint – replace with actual Upstox API endpoint.
        url = f"https://api.upstox.com/market/{symbol}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, headers=headers)
        data = response.json()
        return data.get("last_price", 0.0)

    async def monitor_stock(self, symbol: str, target: float, callback):
        while True:
            price = self.get_stock_price(symbol)
            if price >= target:
                await callback(f"{symbol} crossed target: {price}")
            await asyncio.sleep(5)  # Polling interval; adjust as needed.
