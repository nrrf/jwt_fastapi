from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from db.db_connection import Base, engine
from typing import Optional

class CategoryInDB(Base): 
    __tablename__ = "category"
    idcategory = Column(String, primary_key= True, unique=True,nullable=False)
    descriptioncategory = Column(String, nullable=False)
Base.metadata.create_all(bind=engine) 