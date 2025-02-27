# app/models.py
from pydantic import BaseModel

class Alert(BaseModel):
    symbol: str
    target_price: float
    user_contact: str  # e.g., email or phone number
