from fastapi import FastAPI, APIRouter, status, HTTPException, Depends
from models.userdetail_model import UserDetailsCreate, UserDetailsResponse
from schemas.userdetails_schemas import  UserDetails # These are Pydantic schemas
from services.smtp_email import send_welcome_email
from services.hashed_pasword import hash_password
from sqlalchemy.orm import Session
from database.db import getdb
from fastapi.responses import JSONResponse
from api.v1.endpoints.auth_endpoints import get_current_user
from services.userdetails_services import update_userdetails_data,soft_delete_userdetails_data
from schemas.department_schemas import Department
from schemas.designation_schemas import Designation



userdetails_root = APIRouter()

@userdetails_root.post('/userdetails/register', response_model=UserDetailsResponse)
def register(user: UserDetailsCreate, db: Session = Depends(getdb),current_user: UserDetails = Depends(get_current_user)):
    # Check if the username already exists
    existing_user = db.query(UserDetails).filter(UserDetails.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Check if the email already exists
    existing_email = db.query(UserDetails).filter(UserDetails.email == user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password and create a new user
    try:
        hashed_password = hash_password(user.password)
        db_user = UserDetails(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            fullname=user.fullname,
            emp_id=user.emp_id,
            dept_id=user.dept_id,
            desig_id=user.desig_id
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Send a welcome email
        send_welcome_email(user.email, user.username, user.password)

        # Return a custom response with a success message
        response_content = {
            "message": "User successfully registered",
            "user": {
                "username": db_user.username,
                "email": db_user.email,
                "status": "ok"
            }
        }
        return JSONResponse(content=response_content, status_code=status.HTTP_201_CREATED)

    except Exception as e:
        db.rollback()  # Rollback in case of failure
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while registering the user.")

@userdetails_root.get("/get/userdetails")
def read_userdetails(db: Session = Depends(getdb), current_user: UserDetails = Depends(get_current_user)):
    # Query to join UserDetails with Department and Designation
    user_details = (
        db.query(UserDetails, Department.department_name.label("department_name"), Designation.designation_name.label("designation_name"))
        .join(Department, UserDetails.dept_id == Department.id, isouter=True)  # Use outer join if department is optional
        .join(Designation, UserDetails.desig_id == Designation.id, isouter=True) 
        .filter(UserDetails.status == 1) # Use outer join if designation is optional
        .all()
    )

    if not user_details:
        raise HTTPException(status_code=404, detail="No user details found")

    # Format the results as needed
    results = []
    for user, department_name, designation_name in user_details:
        results.append({
            "username": user.username,
            "fullname": user.fullname,
            "email": user.email,
            "emp_id": user.emp_id,
            "status": user.status,
            "department_name": department_name,
            "designation_name": designation_name,
        })

    return results

@userdetails_root.get("/get/userdetails/{id}")
def read_userdetails(id: int, db: Session = Depends(getdb), current_user: UserDetails = Depends(get_current_user)):
    # Query to join UserDetails with Department and Designation, filtered by user ID
    user_details = (
        db.query(UserDetails, Department.department_name.label("department_name"), Designation.designation_name.label("designation_name"))
        .join(Department, UserDetails.dept_id == Department.id, isouter=True)  # Use outer join if department is optional
        .join(Designation, UserDetails.desig_id == Designation.id, isouter=True)  # Use outer join if designation is optional
        .filter(UserDetails.id == id)
        .first()  # Use .first() to get one record matching the ID
    )

    if not user_details:
        raise HTTPException(status_code=404, detail=f"No user details found for ID {id}")

    # Format the result as needed
    user, department_name, designation_name = user_details

    result = {
        "username": user.username,
        "fullname": user.fullname,
        "email": user.email,
        "emp_id": user.emp_id,
        "status": user.status,
        "department_name": department_name,
        "designation_name": designation_name,
    }

    return result

@userdetails_root.put("/userdetails/update/{id}")
def update_userdetails(id: int, item: UserDetailsCreate, db: Session = Depends(getdb), current_user: UserDetails = Depends(get_current_user)):
    # Find the user by ID
    # user = db.query(UserDetails).filter(UserDetails.id == id).first()
    user = update_userdetails_data(db=db, id=id, dept=item)

    if not user:
        raise HTTPException(status_code=404, detail="User Details not found or inactive")
    else:
    # return new_dept
        response_content = {
            "message": "UserDetail Updated successfully",
            "UserDetail": {
                "fullname": user.fullname,
                "email": user.email,
                "status": "ok"
            }
        }
    return JSONResponse(content=response_content, status_code=status.HTTP_201_CREATED)
   # return {"detail": "Designation successfully updated", "designation": updated_item}



@userdetails_root.patch("/userdetails/soft-delete/{id}")
def soft_delete_department(id: int, db: Session = Depends(getdb), current_user: UserDetails = Depends(get_current_user)):
    updated_item = soft_delete_userdetails_data(db=db, id=id)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="User Details  not found or already inactive")
    
    else:
    # return new_dept
        response_content = {
            "message": "User Details Deleted successfully",
            "UserDetails": {
                "fullname": updated_item.fullname,
                "status": updated_item.status
               
            }
        }
    return JSONResponse(content=response_content, status_code=status.HTTP_201_CREATED)
