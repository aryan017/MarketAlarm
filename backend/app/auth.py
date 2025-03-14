from datetime import datetime, timedelta
from typing import Optional
from pymongo import MongoClient
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



router = APIRouter()
client = MongoClient("mongodb://localhost:27017/")
db = client["user_details"]
users_collection = db["user"]



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(datetime.timezone.utc) + (timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/signup")
async def signup(user : User):
        existing_user=users_collection.find_one({"username" : user.username,"email" : user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
    
        user.hash_password()
        users_collection.insert_one(user.model_dump())
        return {"message": "New User has been created successfully"}


@router.post("/login")
async def login(user: OAuth2PasswordRequestForm = Depends()):
        logged_in_User = users_collection.find_one({"email" : user.email,"password" : user.password})
        if not user or not verify_password(user.password,logged_in_User.password ):
            raise HTTPException(status_code=401, detail="Invalid credentials")
    
        access_token = create_access_token({"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}


@router.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {"message": f"Hello, {username}! This is a protected route."}
