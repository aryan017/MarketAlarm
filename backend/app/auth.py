from datetime import timezone, datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import APIRouter, HTTPException
from jose import jwt
from passlib.context import CryptContext
from app.models import User,Login_Request
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()
client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = client["user_details"]
users_collection = db["user"]



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/signup")
async def signup(user : User):
    try:
        print(user)
        existing_user=await users_collection.find_one({"email" : user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        else :    
            user.hash_password()
            await users_collection.insert_one(user.model_dump())
            return {"message": "New User has been created successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"An unexpected error occurred: {str(e)}")
        


@router.post("/login")
async def login(user: Login_Request):
        logged_in_User = await users_collection.find_one({"email" : user.email})
        if not user or not verify_password(user.password,logged_in_User["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
    
        access_token = create_access_token({"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}



