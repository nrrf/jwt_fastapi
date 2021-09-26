from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.db_connection import get_db
from jose import JWTError, jwt
from passlib.context import CryptContext
from db.user_db import UserInDB, Token, TokenData
from models.user_models import UserRegistrationIn, UserIn, ChangePassword

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter() 

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user_in_db = db.query(UserInDB).get(token_data.username)
    if user_in_db is None:
        raise credentials_exception
    return user_in_db


async def get_current_active_user(current_user: UserIn = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user 


@router.post("/user/registration", response_model = Token)
async def register_user(register_in: UserRegistrationIn, db:Session=Depends(get_db)): 
    user_in_db = db.query(UserInDB).get(register_in.iduser)
    
    if user_in_db != None: 
        raise HTTPException(status_code=404, detail="El usuario ya se encuentra registrado")
    if len(register_in.password)<8: 
        raise HTTPException(status_code=403, detail="Password demasiado corto")

    # obviamente habrian mas restricciones en las q posiblemente se necesite usar regex o metodos similares
    user_add =  UserInDB(**register_in.dict()) 
    print(user_add)
    db.add(user_add)
    db.commit() 
    db.refresh(user_add)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) 

    access_token = create_access_token(
        data={"sub": register_in.iduser}, expires_delta=access_token_expires
    )
    

    return {"access_token": access_token, "token_type": "bearer"}


# el form_data en realidad no es necesario, simpĺemente es una forma de pasar los datos como 
# lo es el regiser_in de arriba
@router.post("/user/login", response_model= Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends() , db:Session=Depends(get_db)): 
    user_in_db = db.query(UserInDB).get(form_data.username) 

    if user_in_db == None:
        raise HTTPException(status_code=404, detail="El cliente no existe")
    if user_in_db.password != form_data.password:
        raise HTTPException(status_code=403, detail="El password no es correcto") 

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) 

    access_token = create_access_token(
        data={"sub": user_in_db.iduser}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Para tener en cuenta: 
"""
async def changepassword(current_user: UserIn = Depends(get_current_active_user), new_password: ChangePassword, db:Session=Depends(get_db)):  
La anterior linea nos va a dar error debido a que current_user tiene un argumento por defecto 
https://careerkarma.com/blog/python-syntaxerror-non-default-argument-follows-default-argument/#:~:text=The%20Python%20%E2%80%9CSyntaxError%3A%20non%2D,come%20after%20non%2Ddefault%20arguments.
"""
@router.put("/user/changepassword")
async def changepassword( new_password: ChangePassword,current_user: UserIn = Depends(get_current_active_user), db:Session=Depends(get_db)): 
    user_in_db = db.query(UserInDB).get(current_user.iduser) 

    if user_in_db == None: 
        raise HTTPException(status_code=500, detail="Error del sistema, intentelo mas tarde")
    if user_in_db.password != current_user.password:
        raise HTTPException(status_code=403, detail="El password no es correcto")
    if len(new_password.new_password)<8: 
        raise HTTPException(status_code=403, detail="New password demasiado corto") 

    user_in_db.password=new_password.new_password
    
    db.commit() 
    db.refresh(user_in_db) 
    return {"New Password": user_in_db.password}

@router.get("/users/me/")
async def read_users_me(current_user: UserIn = Depends(get_current_active_user)):
    return current_user

@router.delete("/users/me/delete") 
async def delete_user(current_user: UserIn = Depends(get_current_active_user), db:Session=Depends(get_db)):  
    user_in_db = db.query(UserInDB).get(current_user.iduser)  
    print(user_in_db)
    db.delete(user_in_db) 
    db.commit()
    return {"Usuario eliminado": True}