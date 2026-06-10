from email.headerregistry import Address
from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel

class Truck(Base):
    __tablename__ = "trucks"

    id = Column(Integer, primary_key=True, index=True)
    item = Column(String, index=True)
    type = Column(String)
    company = Column(String, index=True)


class TruckCreate(BaseModel):
    item: str
    type: str
    company: str

class TruckResponse(BaseModel):
    id: int
    item: str
    type: str
    company: str

    class Config:
        from_attributes = True


""" Table for Drivers
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
"""
