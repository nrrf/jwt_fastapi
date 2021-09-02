from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker 

# Motor y conexion con la base de datos
DATABASE_URL = "postgresql://postgres:nrrf11399@localhost:5432/NRRFPROJECT"
engine= create_engine(DATABASE_URL)

# Creacion sesioni (se conecta con el motor)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine) 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Creando base para la creacion de los esquemas  
Base = declarative_base()
Base.metadata.schema = "trueqapp"