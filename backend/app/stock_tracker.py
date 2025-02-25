import requests
import redis
import time

UPSTOX_API_KEY = "47b39426-9ca5-43ca-9f13-362271c7cede"
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

def fetch_stock_price(symbol):
    """Fetch live stock prices from Upstox API"""
    url = f"https://api.upstox.com/market/v1/quote/{symbol}"
    headers = {"Authorization": f"Bearer {UPSTOX_API_KEY}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        price = data["last_price"]
        redis_client.set(symbol, price)  # Store in Redis
        return price
    return None

if __name__ == "__main__":
    while True:
        stock_price = fetch_stock_price("RELIANCE")
        print(f"Fetched stock price: {stock_price}")
        time.sleep(10)  # Fetch every 10 seconds
