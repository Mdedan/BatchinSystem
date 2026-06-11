from email.headerregistry import Address
from sqlalchemy import Column, Integer, String
from app import Desc
from database import Base
from pydantic import BaseModel

class Delivery(Base):
    __tablename__ = "deliveries"
    id = Column(Integer, primary_key=True, index=True)
    DNo = Column(String, index=True)
    client = Column(String)
    location= Column(String)
    mix_label = Column(String)
    Desc = Column(String)

class DeliveryCreate(BaseModel):
    DNo: str
    client: str
    location: str
    mix_label: str
    Desc: str

class DeliveryResponse(BaseModel):
    id: int
    DNo: str
    client: str
    location: str
    mix_label: str
    Desc: str
    class Config:
        from_attributes = True

