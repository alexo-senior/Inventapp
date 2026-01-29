from pydantic import BaseModel
from typing import Optional

#el filtro de los datos que se van a enviar y recibir a traves de la API
# 1. El esquema base (lo que comparten la creación y la lectura)
class MedicamentoBase(BaseModel):
    nombre: str
    lote: str
    laboratorio: str
    vencimiento: str

# 2. Esquema para CREAR (por ahora es igual al base)
class MedicamentoCreate(MedicamentoBase):
    pass

# 3. Esquema para LEER (lo que la API devuelve al usuario)
class Medicamento(MedicamentoBase):
    id: int

    class Config:
        # Esto es vital: permite que Pydantic lea los modelos de SQLAlchemy
        from_attributes = True