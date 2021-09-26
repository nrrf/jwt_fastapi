from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from db.db_connection import Base, engine
from typing import Optional

class ProductInDB(Base): 
    __tablename__ = "product"

    id_product = Column(Integer, primary_key= True, unique=True, autoincrement=True)
    iduser = Column(String, nullable=False)
    idcategory = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
Base.metadata.create_all(bind=engine) 