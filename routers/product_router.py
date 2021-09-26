from typing import List
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from db.db_connection import get_db 
from routers.user_router import get_current_active_user
from models.user_models import UserRegistrationIn, UserIn, ChangePassword 
from models.product_models import ProductRegistrationIn  
from db.product_db import ProductInDB
from db.category_db import CategoryInDB

router = APIRouter()  

@router.post("/product/registration") 
async def register_product(register_in : ProductRegistrationIn, current_user: UserIn = Depends(get_current_active_user), db:Session=Depends(get_db)):  
    name_product_user = db.query(ProductInDB).filter(ProductInDB.iduser==current_user.iduser,ProductInDB.name==register_in.name).first() 
    if name_product_user==None:
        product = {}  
        product["iduser"] = current_user.iduser 
        for name, value in register_in:
            product[name] = value
        product_add = ProductInDB(**product) 
        db.add(product_add) 
        db.commit() 
        db.refresh(product_add) 
        return {"Producto Registrado": True} 
    else: 
        raise HTTPException(status_code=403, detail="Un Usuario no puede registrar mas de un producto con el mismo nombre") 

@router.get("/product/my-products") 
async def my_products(current_user: UserIn  =  Depends(get_current_active_user), db:Session=Depends(get_db)): 
    my_products_in_db = db.query(ProductInDB).filter(ProductInDB.iduser==current_user.iduser).all() 
    return my_products_in_db 

@router.get("/product/all-products") 
async def all_products(current_user: UserIn  =  Depends(get_current_active_user), db:Session=Depends(get_db)): 
    my_products_in_db = db.query(ProductInDB).filter(ProductInDB.iduser!=current_user.iduser).all() 
    return my_products_in_db

@router.get("/product/category/{category}") 
async def product_category(category: str , current_user: UserIn  =  Depends(get_current_active_user),db: Session=Depends(get_db)): 
    products_by_category = db.query(ProductInDB).filter(ProductInDB.idcategory == category).all() 
    return products_by_category

@router.delete("/product/delete/{name}")
async def product_delete(name: str , current_user: UserIn  =  Depends(get_current_active_user), db: Session=Depends(get_db)): 

    product_in_db = db.query(ProductInDB).filter(ProductInDB.name == name, ProductInDB.iduser==current_user.iduser).first() 

    if(product_in_db != None):
        db.delete(product_in_db)
        db.commit() 
        return {"Producto Eliminado": True} 
    else: 
        raise HTTPException(status_code=403, detail="El usuario no tiene productos con ese nombre") 