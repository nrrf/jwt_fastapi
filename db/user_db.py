from sqlalchemy import Column, Integer, String, Boolean
from db.db_connection import Base, engine
from typing import Optional
from pydantic import BaseModel

class UserInDB(Base): 
    __tablename__ = "USER"

    iduser = Column(String, primary_key= True, unique=True)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    password = Column(String, nullable=False)
    disabled= Column(Boolean, nullable=False)
Base.metadata.create_all(bind=engine) 

class Token(BaseModel): 
    access_token: str 
    token_type: str 
class TokenData(BaseModel): 
    username: Optional[str] = None