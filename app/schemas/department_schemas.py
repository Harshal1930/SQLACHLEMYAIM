from database.db import Base
from sqlalchemy import Column, String,Integer
from sqlalchemy.orm import relationship



class Department(Base):
    __tablename__ = "department"

    id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String(50), unique=True, index=True)
    status = Column(Integer, default=1)  # Default value of 1


