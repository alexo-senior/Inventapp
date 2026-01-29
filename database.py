from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# esta es la direccion de la base de datos 
SQLALCHEMY_DATABASE_URL = "sqlite:///.farmacia.db"

# se crea el motor de la bd 
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    
)
# se crea una sesion local para acceder a la bd

SessionLocal = sessionmaker(autocommit= False, autoflush=False, bind=engine)
Base = declarative_base()




