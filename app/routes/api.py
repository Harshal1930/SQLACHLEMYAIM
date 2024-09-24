from api.v1.endpoints.user_endpoint import user_root
from api.v1.endpoints.department_endpoint import department_root
from fastapi import FastAPI,APIRouter
from api.v1.endpoints.designation_endpoints import designation_root
from api.v1.endpoints.userdetail_endpoints import userdetails_root

api_root = APIRouter()


api_root.include_router(user_root,tags=["Users"])
api_root.include_router(department_root,tags=["Department"])
api_root.include_router(designation_root,tags=["Designation"])
api_root.include_router(userdetails_root,tags=["UserDetails"])