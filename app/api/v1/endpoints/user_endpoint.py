from fastapi import FastAPI, APIRouter, status, HTTPException, Depends
from models.users_model import UserResponse, UserCreate
from schemas.users_schemas import User
from services.smtp_email import send_welcome_email
from services.hashed_pasword import hash_password  
from sqlalchemy.orm import Session
from database.db import getdb
from fastapi.responses import JSONResponse

user_root = APIRouter()

@user_root.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(getdb)):
    # Check if the username already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Check if the email already exists
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password and create a new user
    try:
        hashed_password = hash_password(user.password)
        db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
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
