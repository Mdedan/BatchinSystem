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

@app.post("/trucks", response_model=models.TruckResponse)  
def create_truck(truck: models.TruckCreate, db: Session = Depends(get_db)):
    new_truck = models.Truck(item=truck.item, type=truck.type, company=truck.company)
    db.add(new_truck)
    db.commit()
    db.refresh(new_truck)
    return new_truck

@app.get("/trucks")
def get_all_trucks(db: Session = Depends(get_db)):
    return db.query(models.Truck).all()

