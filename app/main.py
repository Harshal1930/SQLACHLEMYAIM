from fastapi import FastAPI,Depends,HTTPException,status
from routes.api import api_root
from database.db import Base,engine,getdb
from models.users_model import UserCreate,UserResponse
from sqlalchemy.orm import Session
from models.auth_model import Token
from schemas.users_schemas import User
from api.v1.endpoints.auth_endpoints import verify_token,create_access_token,SECRET_KEY,ALGORITHM,get_current_user
from services.hashed_pasword import verify_password
from jose import JWTError,jwt
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from services.redis_services import add_token_to_blacklist

app = FastAPI() 

Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(api_root)

@app.post("/token", response_model=Token)
def login(form_data: UserCreate, db: Session = Depends(getdb)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str, db: Session = Depends(getdb)):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create new access token
    access_token = create_access_token(data={"sub": username})

    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    add_token_to_blacklist(token)
    return {"message": "Successfully logged out"}








