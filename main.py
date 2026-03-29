from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from sqlalchemy import asc
import json



import model 
import schema
import database

# Inicialización de tablas
database.Base.metadata.create_all(bind=database.engine)


app = FastAPI(title="InventApp Gestión de inventario y vencimientos de Medicamentos")

# Función de dependencia para obtener la sesión de la DB

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# RUTAS 

@app.get("/")
def home():
    return {"mensaje": "Bienvenido a InventApp"}



# listar por rango de fecha de vencimiento
# al noincluir los argumentos en la URL sino en la funcion 
# se interpreta como como parametro de consulta fecha inicio y fecha final
@app.get("/medicamentos/rango-vencimiento/", response_model=List[schema.Medicamento])
def obtener_rango_vencimiento(fecha_inicio: str, 
                            fecha_final: str, 
                            db: Session = Depends(get_db)
                            ):
    resultados =db.query(model.Medicamento).filter(
        model.Medicamento.vencimiento.between(fecha_inicio, fecha_final)
    ).order_by(asc(model.Medicamento.vencimiento)).all()
    
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron medicamentos entre {fecha_inicio} y {fecha_final}")
    return resultados

    

# Listar todo

@app.get("/medicamentos", response_model=List[schema.Medicamento])
def obtener_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # skip: cuántos registros saltar
    # limit: cuántos registros mostrar
    return db.query(model.Medicamento).offset(skip).limit(limit).all()


# Sistema de alertas para fechas de vencimiento

@app.get("/medicamentos/alertas", response_model=schema.ResumenAlertas)
def obtener_alertas(db: Session = Depends(get_db)):
    hoy = datetime.now().date()
    fecha_limite = hoy + timedelta(days=180)
    
    # se obtienen todos los registros de la DB
    # se hace el filtrado con las fechas menor o igual a la fecha limite
    
    medicamentos = db.query(model.Medicamento).filter(
        model.Medicamento.vencimiento <= str(fecha_limite)
    ).order_by(asc(model.Medicamento.vencimiento)).all()
    
    vencidos = 0
    por_vencer = 0
    lista_detalles = [] # lista que espera las alertas

    for m in medicamentos:
        # se convierte el texto "YYYY-MM-DD" a un objeto de fecha real
        fecha_venc = datetime.strptime(m.vencimiento, "%Y-%m-%d").date()
        dias_restantes = (fecha_venc - hoy).days
        
        # se hace el filtro 
        # Clasificamos la gravedad
        
        if dias_restantes < 0:
            status = "VENCIDO REPORTAR Y DESTRUIR"
            vencidos += 1
            
            # critico de 0 a 35 dias
        elif 0 <= dias_restantes <= 35:
            status = "CRÍTICO / RETIRO INMINENTE"
            por_vencer += 1
            
            # proximo mes de 36 a 65 dias     
        elif 11 <= dias_restantes <= 65:
            status = "ALERTA / PRÓXIMOS 1-2 MESES"
            por_vencer += 1
            
            # por politica de devolucion     
        else:
            status = "GESTIÓN DE DEVOLUCIÓN (POLÍTICA)" 
            por_vencer += 1
            
            # Creamos el objeto de respuesta
        lista_detalles.append(schema.AlertaMedicamento(
            **m.__dict__, # copia todos los campos base automáticamente
            dias_para_vencer=dias_restantes,
            estado=status    
            
        ))
            
    return {
        "total_vencidos": vencidos,
        "total_por_vencer": por_vencer,
        "detalles": lista_detalles
    }



# Buscar por ID
@app.get("/medicamentos/{id}", response_model=schema.Medicamento)
def obtener_por_id(id: int, db: Session = Depends(get_db)):
    medicamento = db.query(model.Medicamento).filter(model.Medicamento.id == id).first()
    if not medicamento:
        raise HTTPException(status_code=404, detail="Medicamento no encontrado")
    return medicamento

# Buscar por Nombre
@app.get("/medicamentos/nombre/{nombre}", response_model=List[schema.Medicamento])
def obtener_por_nombre(nombre: str, db: Session = Depends(get_db)):
    
    # Usamos .ilike para que no importe si es mayúscula o minúscula
    resultados = db.query(model.Medicamento).filter(model.Medicamento.nombre.ilike(f"%{nombre}%")).all()
    return resultados

# Listar por Laboratorio
@app.get("/medicamentos/laboratorio/{lab}", response_model=List[schema.Medicamento])
def obtener_por_laboratorio(lab: str, db: Session = Depends(get_db)):
    resultados = db.query(model.Medicamento).filter(model.Medicamento.laboratorio.ilike(f"%{lab}%")).all()
    if not resultados:
        raise HTTPException(status_code=404, detail=f"No hay productos de {lab}")
    return resultados



import json

def carga_maestra():
    db = database.SessionLocal()
    try:
        if db.query(model.Medicamento).count() == 0:
            # Leer el archivo externo
            with open("medicamentos.json", "r", encoding="utf-8") as f:
                datos_farma = json.load(f)
            
            # Usar desempaquetado de diccionarios (**) para crear los objetos
            productos = [model.Medicamento(**item) for item in datos_farma]
            
            db.add_all(productos)
            db.commit()
            print(f"--- CARGA EXITOSA: {len(productos)} registros desde JSON ---")
    except Exception as e:
        db.rollback()
        print(f"Error al leer el archivo JSON: {e}")
    finally:
        db.close()
carga_maestra()
print("Servidor listo, base de datos cargada y verificada.")

