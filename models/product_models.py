from pydantic import BaseModel 

class ProductRegistrationIn(BaseModel): 
    idcategory: str
    name: str 
    description: str 