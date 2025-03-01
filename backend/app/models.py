from pydantic import BaseModel

class Alert(BaseModel):
    symbol: str
    target_price: float
    user_contact: str  
