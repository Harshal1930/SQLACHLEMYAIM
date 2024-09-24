from pydantic import BaseModel,Field,field_validator

class DepartmentCreate(BaseModel):
      
       department_name:str
       status: int = Field(default=1)  # Default value of 1


#to show or store only 0,1 value 
@field_validator('status')
def check_status(cls, v):
    if v not in (0, 1):
        raise ValueError('Status must be 0 or 1')
    return v

class DepartmentResponse(BaseModel):
      
       id:int
       department_name:str
       status: int

class config:
      
    from_attributes = True 