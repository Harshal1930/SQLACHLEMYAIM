from sqlalchemy.orm import Session
from models.department_model import DepartmentCreate,DepartmentResponse
from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI,HTTPException
from sqlalchemy import asc
from schemas.department_schemas import Department

def create_item(db: Session, dept: DepartmentCreate):
    # Check if department name already exists
    existing_dept = db.query(Department).filter(Department.department_name == dept.department_name).first()
    if existing_dept:
        raise HTTPException(
            status_code=400,
            detail="Department with this name already exists"
        )

    db_dept = Department(**dept.model_dump())
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
    return db.query(Department).filter(Department.status == 1).order_by(asc(Department.id)).all()

def get_item(db: Session, id: int):
    return db.query(Department).filter(Department.id == id, Department.status == 1).first()

def update_department_data(db: Session, id: int, dept: DepartmentCreate):
    # Find the department by id where status is 1 (active)
    department = db.query(Department).filter(Department.id == id, Department.status == 1).first()

    if not department:
        return None  # Return None if department not found or status is not active

    # Update department fields with new data
    department.department_name = dept.department_name
     # Assuming you have this field
    # Add other fields as necessary
    
    try:
        # Commit the changes
        db.commit()
        db.refresh(department)  # Refresh to get the updated object
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while updating the department")
    
    return department  # Return the updated department

def soft_delete_department_data(db: Session, id: int):
    # Find the department by id where status is 1 (active)
    department = db.query(Department).filter(Department.id == id, Department.status == 1).first()

    if not department:
        return None  # Return None if department not found or is already inactive

    # Change the status to 0 (soft delete)
    department.status = 0

    try:
        # Commit the changes
        db.commit()
        db.refresh(department)  # Refresh to get the updated object
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while soft deleting the department")
    
    return department  # Return the soft-deleted department