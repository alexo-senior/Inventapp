from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# esta es la direccion de la base de datos 
#SQLALCHEMY_DATABASE_URL = "sqlite:///.farmacia.db"
DB_NAME = "gestion_farmacia"
SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:root@127.0.0.1:3306/gestion_farmacia'

# se crea el motor de la bd 
"""
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    
)
"""
#para mysql no se necesita el argumento connect_args
#asi mantiene hast 10 cioenxiones extra si hay mucho trafico 
# y 5 conexiones abiertas listas para usar

engine = create_engine(SQLALCHEMY_DATABASE_URL,pool_size=5,max_overflow=10)         # Mantiene 5 conexiones abiertas listas para usar

# se crea una sesion local para acceder a la bd

SessionLocal = sessionmaker(autocommit= False, autoflush=False, bind=engine)

Base = declarative_base()




