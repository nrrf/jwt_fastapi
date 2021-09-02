from pydantic import BaseModel

class UserRegistrationIn(BaseModel):
    iduser : str
    email : str
    phone : str
    password: str

class UserIn(BaseModel): 
    iduser : str 
    password : str  
    disabled: bool

class NewUserPassword(BaseModel): 
    iduser : str 
    password : str 
    newpassword: str

class UserOut(BaseModel): 
    email: str 
    phone: str
    class Config:
        orm_mode = True