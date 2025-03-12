import asyncio
import httpx
import json

class UpstoxClient:
    def __init__(self, api_key: str = None, access_token: str = None):
        self.api_key = api_key 
        self.access_token = access_token 

        if not self.api_key or not self.access_token:
            raise ValueError("API Key and Access Token must be set either via arguments or environment variables.")

    async def get_stock_detail(self, symbol: str) -> dict:
        formatted_symbol = f"NSE_EQ|{symbol}"
        url = f"https://api.upstox.com/v2/market-quote/quotes?instrument_key={formatted_symbol}"  
        headers = {"Authorization": f"Bearer {self.access_token}","Accept": "application/json"}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, timeout=10)
                response.raise_for_status() 
                return response.json()
            except httpx.HTTPStatusError as http_err:
                print(f"HTTP error fetching {symbol}: {http_err}")
            except httpx.RequestError as req_err:
                print(f"Request error fetching {symbol}: {req_err}")
            except Exception as err:
                print(f"Unexpected error fetching {symbol}: {err}")

        return {}

    async def monitor_stock(self, symbol: str, target: float, callback):
        alert_sent = False
        while True:
            res = await self.get_stock_detail(symbol)  
            print(res)
            stock_symbol = next(iter(res['data']))
            stock=res["data"][stock_symbol]["symbol"]
            price=res["data"][stock_symbol]["last_price"]
            print(price)
            print(target)
            if not alert_sent and price >= target:
                try:
                    await callback(f"{stock} crossed target price: Rs {target} by Current Price: Rs {price}")
                    alert_sent = True 
                except Exception as e:
                    print(f"Error in callback: {e}")

            await asyncio.sleep(5)  # Polling interval


