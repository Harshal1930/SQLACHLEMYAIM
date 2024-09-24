from database.db import Base
from sqlalchemy import Column,String,Integer


class Designation(Base):
    __tablename__ = 'designation'

    id = Column(Integer,primary_key=True,index=True )
    designation_name = Column(String(50),unique=True,index=True)
    status = Column(Integer,default=1)

    # designations = relationship("UserDetails", back_populates="userdetails")

