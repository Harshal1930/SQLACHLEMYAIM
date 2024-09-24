from fastapi import FastAPI,APIRouter,Depends,HTTPException,status
from models.department_model import DepartmentCreate,DepartmentResponse
from services.department_services import create_item,get_items,get_item,update_department_data,soft_delete_department_data
from sqlalchemy.orm import Session
from database.db import getdb
from schemas.users_schemas import User
from api.v1.endpoints.auth_endpoints import get_current_user
from fastapi.responses import JSONResponse



department_root = APIRouter()

@department_root.post("/departments/create")
def create_department(item: DepartmentCreate, db: Session = Depends(getdb)):
    new_dept = create_item(db=db, dept=item)
    if new_dept is None:
        raise HTTPException(
            status_code=400,
            detail="Department creation failed"
        )
    else:
    # return new_dept
        response_content = {
            "message": "Depaartment successfully registered",
            "Department": {
                "department": new_dept.department_name,
                "status": "ok"
            }
        }
    return JSONResponse(content=response_content, status_code=status.HTTP_201_CREATED)

@department_root.get("/get/departments")
def read_items(db: Session = Depends(getdb), current_user: User = Depends(get_current_user)):
  return get_items(db)

@department_root.get("/department/{id}")
def read_item(id: int,db: Session = Depends(getdb), current_user: User = Depends(get_current_user)):
    dept = get_item(db, id=id)
    if dept is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept

@department_root.put("/department/update/{id}")
def update_department(id: int, item: DepartmentCreate, db: Session = Depends(getdb), current_user: User = Depends(get_current_user)):
    updated_item = update_department_data(db=db, id=id, dept=item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Department not found or inactive")
    
    else:
    # return new_dept
        response_content = {
            "message": "Department Updated successfully",
            "Department": {
                "department": updated_item.department_name,
                "status": "ok"
            }
        }
    return JSONResponse(content=response_content, status_code=status.HTTP_201_CREATED)
   # return {"detail": "Department successfully updated", "department": updated_item}


@department_root.patch("/department/soft-delete/{id}")
def soft_delete_department(id: int, db: Session = Depends(getdb), current_user: User = Depends(get_current_user)):
    updated_item = soft_delete_department_data(db=db, id=id)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Department not found or already inactive")
    
    else:
    # return new_dept
        response_content = {
            "message": "Department Deleted successfully",
            "Department": {
                "department": updated_item.department_name,
                "status": updated_item.status
               
            }
        }
    return JSONResponse(content=response_content, status_code=status.HTTP_201_CREATED)

