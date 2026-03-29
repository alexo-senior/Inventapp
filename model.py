from sqlalchemy import Column, Integer, String, Float
import database 

class Medicamento(database.Base):
    __tablename__ = "inventario"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), index=True)
    lote = Column(String(50), unique=True, index=True)
    laboratorio = Column(String(100))
    vencimiento = Column(String(10)) # Formato YYYY-MM-DD
    stock = Column(Integer, default=0)
    precio = Column(Float, default=0.0) 