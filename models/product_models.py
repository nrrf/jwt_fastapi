from pydantic import BaseModel 

class ProductRegistrationIn(BaseModel): 
    name: str 
    description: str 