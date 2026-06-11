from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, get_db, Base # <--- All imported from database.py! Connections 
import models                              # <--- Imported from models.py! (Schema)

app = FastAPI()

# Creates the tables using the centralized engine and models
Base.metadata.create_all(bind=engine)

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"status": "healthy", "message": "Backend is running!"}

@app.post("/deliveries", response_model=models.DeliveryResponse)
def create_delivery(delivery: models.DeliveryCreate, db: Session = Depends(get_db)):
    new_delivery = models.Delivery(DNo=delivery.DNo, client=delivery.client, location=delivery.location, mix_label=delivery.mix_label, Desc=delivery.Desc)
    db.add(new_delivery)
    db.commit()
    db.refresh(new_delivery)
    return new_delivery

@app.get("/deliveries")
def get_all_deliveries(db: Session = Depends(get_db)):
    return db.query(models.Delivery).all()


