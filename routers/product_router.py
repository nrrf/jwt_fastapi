from typing import List
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from db.db_connection import get_db 
from routers.user_router import get_current_active_user
from models.user_models import UserRegistrationIn, UserIn, ChangePassword 
from models.product_models import ProductRegistrationIn  
from db.product_db import ProductInDB

router = APIRouter()  

@router.post("/product/registration") 
async def register_product(register_in : ProductRegistrationIn, current_user: UserIn = Depends(get_current_active_user), db:Session=Depends(get_db)): 
    product = {}  
    product["id_user"] = current_user.iduser 
    for name, value in register_in:
        product[name] = value
    product_add = ProductInDB(**product) 
    db.add(product_add) 
    db.commit() 
    db.refresh(product_add) 
    return {"Producto Registrado": True}

@router.get("/product/my-products") 
async def my_products(current_user: UserIn  =  Depends(get_current_active_user), db:Session=Depends(get_db)): 
    my_products_in_db = db.query(ProductInDB).filter(ProductInDB.id_user==current_user.iduser).all() 
    return my_products_in_db 

@router.get("/product/all-products") 
async def all_products(current_user: UserIn  =  Depends(get_current_active_user), db:Session=Depends(get_db)): 
    my_products_in_db = db.query(ProductInDB).filter(ProductInDB.id_user!=current_user.iduser).all() 
    return my_products_in_db