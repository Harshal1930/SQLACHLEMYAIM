from fastapi import FastAPI,HTTPException
from sqlalchemy.orm import Session
from models.designation_model import DesignationCreate
from schemas.designation_schemas import Designation
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc




def create_designation(db:Session, desg:DesignationCreate):
    existing_desg = db.query(Designation).filter(Designation.designation_name == desg.designation_name).first()
    if existing_desg:
        raise HTTPException(
            status_code=400,
            detail="Designation with this name already exists"
        )
    
    db_desg = Designation(**desg.model_dump())
    db.add(db_desg)
    try:
        db.commit()
        db.refresh(db_desg)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the department"
        )
    return db_desg

def get_items(db: Session):
#     #return db.query(Department).order_by(asc(Department.id)).all();
    return db.query(Designation).filter(Designation.status == 1).order_by(asc(Designation.id)).all()

def get_item(db: Session, id: int):
    return db.query(Designation).filter(Designation.id == id, Designation.status == 1).first()

def update_designation_data(db: Session, id: int, desg: DesignationCreate):
    # Find the designation by id where status is 1 (active)
    designation = db.query(Designation).filter(Designation.id == id, Designation.status == 1).first()

    if not designation:
        return None  # Return None if designation not found or status is not active

    # Update designation fields with new data
    designation.designation_name = desg.designation_name
     # Assuming you have this field
    # Add other fields as necessary
    
    try:
        # Commit the changes
        db.commit()
        db.refresh(designation)  # Refresh to get the updated object
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while updating the department")
    
    return designation  # Return the updated designation

def soft_delete_designation_data(db: Session, id: int):
    # Find the department by id where status is 1 (active)
    designation = db.query(Designation).filter(Designation.id == id, Designation.status == 1).first()

    if not designation:
        return None  # Return None if department not found or is already inactive

    # Change the status to 0 (soft delete)
    designation.status = 0

    try:
        # Commit the changes
        db.commit()
        db.refresh(designation)  # Refresh to get the updated object
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while soft deleting the designation")
    
    return designation  # Return the soft-deleted department