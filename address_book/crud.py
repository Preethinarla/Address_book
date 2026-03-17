from sqlalchemy.orm import Session
from . import models, schemas

def create_address(db: Session, address: schemas.AddressCreate) -> models.Address:
    db_obj = models.Address(**address.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_addresses(db: Session) -> list[models.Address]:
    return db.query(models.Address).all()

def get_address(db: Session, address_id: int) -> models.Address | None:
    return db.query(models.Address).filter(models.Address.id == address_id).first()

def update_address(db: Session, address_id: int, data: schemas.AddressUpdate):
    db_obj = get_address(db, address_id)
    if not db_obj:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(db_obj, key, value)

    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_address(db: Session, address_id: int):
    db_obj = get_address(db, address_id)
    if not db_obj:
        return None

    db.delete(db_obj)
    db.commit()
    return db_obj