from pydantic import BaseModel,Field,field_validator

class DesignationCreate(BaseModel):

    designation_name:str
    status: int = Field(default=1)

    @field_validator('status')
    def check_status(cls,v):
        if v not in (0, 1):
            raise ValueError('Status must be 0 or 1')
        return v
    
    class DesignationResponse(BaseModel):

        id:int
        designation_name:str
        status: int
    
    class config:

        from_attributes = True