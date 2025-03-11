import asyncio
import httpx
import json

class UpstoxClient:
    def __init__(self, api_key: str = None, access_token: str = None):
        self.api_key = api_key 
        self.access_token = access_token 

        if not self.api_key or not self.access_token:
            raise ValueError("API Key and Access Token must be set either via arguments or environment variables.")

    async def get_stock_price(self, symbol: str) -> float:
        formatted_symbol = f"NSE_EQ|{symbol}"
        url = f"https://api.upstox.com/v2/market-quote/quotes?instrument_key={formatted_symbol}"  
        headers = {"Authorization": f"Bearer {self.access_token}","Accept": "application/json"}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, timeout=10)
                response.raise_for_status() 
                res=json.loads(json.dumps(response.json()))
                symbol = next(iter(res['data']))
                return res["data"][symbol]["last_price"]
            except httpx.HTTPStatusError as http_err:
                print(f"HTTP error fetching {symbol}: {http_err}")
            except httpx.RequestError as req_err:
                print(f"Request error fetching {symbol}: {req_err}")
            except Exception as err:
                print(f"Unexpected error fetching {symbol}: {err}")

        return 0.0  

    async def monitor_stock(self, symbol: str, target: float, callback):
        while True:
            price = await self.get_stock_price(symbol)  
            print(price)
            print(target)
            if price >= target:
                try:
                    await callback(f"{symbol} crossed target: {price}")
                except Exception as e:
                    print(f"Error in callback: {e}")
            await asyncio.sleep(5)  # Polling interval


