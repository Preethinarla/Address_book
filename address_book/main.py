from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from geopy.distance import geodesic

from .database import SessionLocal, engine, Base
from . import crud, schemas
from .logger import log_handle 
import sys, os

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Address Book API", version="1.0")
logger = log_handle()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE
@app.post("/addresses", response_model=schemas.AddressOut)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    logger.info("Creating new address")
    return crud.create_address(db, address)

# READ ALL
@app.get("/addresses", response_model=list[schemas.AddressOut])
def get_addresses(db: Session = Depends(get_db)):
    logger.info("Fetching all addresses")
    return crud.get_addresses(db)

# UPDATE
@app.put("/addresses/{id}", response_model=schemas.AddressOut)
def update_address(id: int, data: schemas.AddressUpdate, db: Session = Depends(get_db)):
    logger.info(f"Updating address {id}")
    updated = crud.update_address(db, id, data)

    if not updated:
        logger.error("Address not found")
        raise HTTPException(status_code=404, detail="Address not found")

    return updated

# DELETE
@app.delete("/addresses/{id}")
def delete_address(id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Deleting address {id}")
        deleted = crud.delete_address(db, id)

        if not deleted:
            logger.error("Address not found")
            raise HTTPException(status_code=404, detail="Address not found")

        return {"message": "Deleted successfully"}
    
    except Exception as e:
        line_no = sys.exc_info()[-1].tb_lineno 
        logger.error("Error occured at" , line_no , str(e))
    

# NEARBY
@app.get("/addresses/nearby", response_model=list[schemas.AddressOut])
def get_nearby(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    distance: float = Query(5, gt=0),
    db: Session = Depends(get_db)): 
    
    try:
        logger.info(f"Finding nearby addresses within {distance} km")

        addresses = crud.get_addresses(db)
        result = []

        for addr in addresses:
            dist = geodesic((lat, lon), (addr.latitude, addr.longitude)).km

            if dist <= distance:
                result.append(addr)

        return result 
    except Exception as e:
        line_no = sys.exc_info()[-1].tb_lineno 
        logger.error("Error occured at" , line_no , str(e))
        