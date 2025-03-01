import asyncio
import httpx


class UpstoxClient:
    def __init__(self, api_key: str = None, access_token: str = None):
        self.api_key = api_key 
        self.access_token = access_token 

        if not self.api_key or not self.access_token:
            raise ValueError("API Key and Access Token must be set either via arguments or environment variables.")

    async def get_stock_price(self, symbol: str) -> float:
        url = f"https://api.upstox.com/market/{symbol}"  # Ensure this is correct
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, timeout=10)
                response.raise_for_status()  # Raise an error for 4xx/5xx responses
                data = response.json()
                return data.get("last_price", 0.0)
            except httpx.HTTPStatusError as http_err:
                print(f"HTTP error fetching {symbol}: {http_err}")
            except httpx.RequestError as req_err:
                print(f"Request error fetching {symbol}: {req_err}")
            except Exception as err:
                print(f"Unexpected error fetching {symbol}: {err}")

        return 0.0  # Return 0.0 if request fails

    async def monitor_stock(self, symbol: str, target: float, callback):
        while True:
            price = await self.get_stock_price(symbol)  # Use async method
            if price >= target:
                try:
                    await callback(f"{symbol} crossed target: {price}")
                except Exception as e:
                    print(f"Error in callback: {e}")
            await asyncio.sleep(5)  # Polling interval


