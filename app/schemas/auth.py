from pydantic import BaseModel,Field



class LoginBase(BaseModel):
    username:str
    password:str = Field(...,min_length=8,max_length=32)

