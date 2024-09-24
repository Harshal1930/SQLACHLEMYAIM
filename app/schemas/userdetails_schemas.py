from fastapi import FastAPI
from sqlalchemy import Column,Integer,String,ForeignKey
from database.db import Base

class UserDetails(Base):
    __tablename__ = 'userdetails'

    id = Column(Integer,primary_key=True,index=True)
    username = Column(String(50),unique=True,index=True)
    hashed_password= Column(String(50),unique=True)
    fullname = Column(String(50),index=True)
    email = Column(String(50),index=True)
    emp_id = Column(Integer,index=True)
    status = Column(Integer,default=1)

    from schemas.department_schemas import Department
    from schemas.designation_schemas import Designation

    dept_id = Column(Integer,ForeignKey(Department.id),index=True)
    desig_id = Column(Integer,ForeignKey(Designation.id),index=True)