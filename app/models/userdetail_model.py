from pydantic import BaseModel,Field,field_validator,EmailStr

class UserDetailsCreate(BaseModel):

    id : int
    username: str
    password : str
    fullname : str
    dept_id : int
    desig_id : int
    email : str
    emp_id : int
    status: int = Field(default=1)
   

    @field_validator('status')
    def check_status(cls,v):
        if v not in (0,1):
            raise ValueError('Status must  be 0 or 1')
        return v
    
class UserDetailsResponse(BaseModel):
    id:int
    username: str
    fullname : str
    dept_id : int
    desig_id : int
    email : EmailStr
    emp_id : int
    status : int

class config:
    from_attributes = True