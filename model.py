from sqlalchemy import Column, Integer, String
import database 

class Medicamento(database.Base):
    __tablename__ = "inventario"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    lote = Column(String, unique=True, index=True)
    laboratorio = Column(String)
    vencimiento = Column(String) # Guardaremos la fecha como texto ISO (YYYY-MM-DD)