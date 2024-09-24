from fastapi import FastAPI,APIRouter,HTTPException,Depends,status
from models.designation_model import DesignationCreate
from sqlalchemy.orm import Session
from database.db import getdb
from services.designation_services import create_designation,get_items,get_item,update_designation_data,soft_delete_designation_data
from fastapi.responses import JSONResponse
from api.v1.endpoints.auth_endpoints import get_current_user
from schemas.users_schemas import User


designation_root = APIRouter()

@designation_root.post('/designation/create')
def create_department(item: DesignationCreate, db: Session = Depends(getdb)):
    new_desig = create_designation(db=db, desg=item)
    if new_desig is None:
        raise HTTPException(
            status_code=400,
            detail="Designation  creation failed"
        )
    else:
    # return new_dept
        response_content = {
            "message": "Designation  successfully Created",
            "Designation": {
                "department": new_desig.designation_name,
                "status": "ok"
            }
        }
    return JSONResponse(content=response_content, status_code=status.HTTP_201_CREATED)

@designation_root.get("/get/designation")
def read_designation(db: Session = Depends(getdb), current_user: User = Depends(get_current_user)):
  return get_items(db)

@designation_root.get("/designation/{id}")
def read_item(id: int,db: Session = Depends(getdb), current_user: User = Depends(get_current_user)):
    desg = get_item(db, id=id)
    if desg is None:
        raise HTTPException(status_code=404, detail="Designation not found")
    return desg

@designation_root.put("/designation/update/{id}")
def update_designation(id: int, item: DesignationCreate, db: Session = Depends(getdb), current_user: User = Depends(get_current_user)):
    updated_item = update_designation_data(db=db, id=id, desg=item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Designation not found or inactive")
    
    else:
    # return new_dept
        response_content = {
            "message": "Designation Updated successfully",
            "Designation": {
                "designation": updated_item.designation_name,
                "status": "ok"
            }
        }
    return JSONResponse(content=response_content, status_code=status.HTTP_201_CREATED)
   # return {"detail": "Designation successfully updated", "designation": updated_item}


@designation_root.patch("/designation/soft-delete/{id}")
def soft_delete_department(id: int, db: Session = Depends(getdb), current_user: User = Depends(get_current_user)):
    updated_item = soft_delete_designation_data(db=db, id=id)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Designation not found or already inactive")
    
    else:
    # return new_dept
        response_content = {
            "message": "Designation Deleted successfully",
            "Designation": {
                "designation": updated_item.designation_name,
                "status": updated_item.status
               
            }
        }
    return JSONResponse(content=response_content, status_code=status.HTTP_201_CREATED)


