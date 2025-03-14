from pydantic import BaseModel,EmailStr
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Alert(BaseModel):
    symbol: str
    target_price: float
    user_contact: str  
    
class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    profession: str
    
    def hash_password(self):
        self.password = pwd_context.hash(self.password)
    
