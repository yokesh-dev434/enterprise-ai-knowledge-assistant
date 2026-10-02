from pydantic import BaseModel,Field

class login_Credtail_request(BaseModel):
    user_name :str
    password : str =Field(min_length=8,max_length=16)