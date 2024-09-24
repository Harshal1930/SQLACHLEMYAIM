from sqlalchemy.orm import Session
from models.userdetail_model import UserDetailsCreate,UserDetailsResponse
from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI,HTTPException
from sqlalchemy import asc
from schemas.userdetails_schemas import UserDetails

def create_item(db: Session, userdetail: UserDetailsCreate):
    # Check if department name already exists
    existing_dept = db.query(UserDetails).filter(UserDetails.fullname == userdetail.fullname).first()
    if existing_dept:
        raise HTTPException(
            status_code=400,
            detail="UserDetails with this name already exists"
        )

    db_dept = userdetail(**userdetail.model_dump())
    db.add(db_dept)
    try:
        db.commit()
        db.refresh(db_dept)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the department"
        )

    return db_dept

def get_items(db: Session):
#     #return db.query(Department).order_by(asc(Department.id)).all();
    return db.query(UserDetails).filter(UserDetails.status == 1).order_by(asc(UserDetails.id)).all()

def get_item(db: Session, id: int):
    return db.query(UserDetails).filter(UserDetails.id == id, UserDetails.status == 1).first()

def update_userdetails_data(db: Session, id: int, dept: UserDetailsCreate):
    # Find the department by id where status is 1 (active)
    userdetails = db.query(UserDetails).filter(UserDetails.id == id, UserDetails.status == 1).first()

    if not userdetails:
        return None  # Return None if department not found or status is not active

    # Update department fields with new data
    userdetails.username  = dept.username,
    userdetails.fullname = dept.fullname,
    userdetails.email = dept.email,
    userdetails.emp_id = dept.emp_id,
    userdetails.dept_id = dept.dept_id,
    userdetails.desig_id = dept.desig_id
     # Assuming you have this field
    # Add other fields as necessary
    
    try:
        # Commit the changes
        db.commit()
        db.refresh(userdetails)  # Refresh to get the updated object
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while updating the UserDetails")
    
    return userdetails  # Return the updated department

def soft_delete_userdetails_data(db: Session, id: int):
    # Find the department by id where status is 1 (active)
    userdetails = db.query(UserDetails).filter(UserDetails.id == id, UserDetails.status == 1).first()

    if not userdetails:
        return None  # Return None if department not found or is already inactive

    # Change the status to 0 (soft delete)
    userdetails.status = 0

    try:
        # Commit the changes
        db.commit()
        db.refresh(userdetails)  # Refresh to get the updated object
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while soft deleting the userdetails")
    
    return userdetails  # Return the soft-deleted department