from pydantic import BaseModel
from typing import Optional, List

#el filtro de los datos que se van a enviar y recibir a traves de la API
# 1. El esquema base (comparten la creación y la lectura)
class MedicamentoBase(BaseModel):
    nombre: str
    lote: str
    laboratorio: str
    vencimiento: str

#  Esquema para CREAR
class MedicamentoCreate(MedicamentoBase):
    pass

# Esquema para LEER (informacion que devuelve al usuario)
class Medicamento(MedicamentoBase):
    id: int
    
class AlertaMedicamento(Medicamento):
    dias_para_vencer: int
    estado: str 
    
    
class ResumenAlertas(BaseModel):
    total_vencidos: int
    total_por_vencer: int
    detalles: List[AlertaMedicamento]

    

    class Config:
        # permite que Pydantic lea los modelos de SQLAlchemy
        from_attributes = True