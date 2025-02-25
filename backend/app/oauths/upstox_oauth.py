from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
import requests
import os
from dotenv import load_dotenv
import secrets

load_dotenv()

app = FastAPI()

# Load environment variables
UPSTOX_API_KEY = os.getenv("UPSTOX_API_KEY")
UPSTOX_API_SECRET = os.getenv("UPSTOX_API_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# Upstox OAuth URLs
UPSTOX_AUTH_URL = "https://api.upstox.com/v2/login/authorization/dialog"
UPSTOX_TOKEN_URL = "https://api.upstox.com/v2/login/authorization/token"

# In-memory storage for state tokens (use Redis or DB in production)
state_tokens = {}

@app.get("/login")
def login():
    """Redirect user to Upstox OAuth authorization URL with state"""
    # Generate a secure random state token
    state = secrets.token_urlsafe(16)
    state_tokens[state] = True  # Store state (for validation later)

    auth_url = (
        f"{UPSTOX_AUTH_URL}?response_type=code&client_id={UPSTOX_API_KEY}"
        f"&redirect_uri={REDIRECT_URI}&response_type=code"
        f"&state={state}"
    )
    return RedirectResponse(auth_url)

@app.get("/callback")
def callback(request: Request):
    """Handle the callback from Upstox with authorization code and verify state"""
    code = request.query_params.get("code")
    state = request.query_params.get("state")

    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not found")

    if not state or state not in state_tokens:
        raise HTTPException(status_code=400, detail="Invalid or missing state parameter")

    # State is valid, remove it to prevent reuse
    del state_tokens[state]

    # Exchange authorization code for access token
    token_data = {
        "code": code,
        "client_id": UPSTOX_API_KEY,
        "client_secret": UPSTOX_API_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    response = requests.post(UPSTOX_TOKEN_URL, data=token_data)

    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info.get("access_token")
        return JSONResponse({"access_token": access_token, "details": token_info})
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Token exchange failed: {response.text}"
        )

