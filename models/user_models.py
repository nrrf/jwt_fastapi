from pydantic import BaseModel

class UserRegistrationIn(BaseModel):
    iduser : str
    email : str
    phone : str
    password: str 
    disabled: bool

class UserIn(BaseModel): 
    iduser : str 
    password : str  
    disabled: bool 

class ChangePassword(BaseModel): 
    new_password: str 
