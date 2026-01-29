from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta



import model 
import schema
import database

# Inicialización de tablas
model.database.Base.metadata.create_all(bind=database.engine)


app = FastAPI(title="InventApp Gestión Profesional de inventarios de Medicamentos")

# 2. Función de dependencia para obtener la sesión de la DB

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

# Listar todo
@app.get("/medicamentos", response_model=List[schema.Medicamento])
def obtener_todos(db: Session = Depends(get_db)):
    return db.query(model.Medicamento).all()


# Sistema de alertas para fechas de vencimiento

@app.get("/medicamentos/alertas", response_model=List[schema.AlertaMedicamento])
def obtener_alertas(db: Session = Depends(get_db)):
    hoy = datetime.now().date()
    #limite_alerta = hoy + timedelta(days=30)
    
    # 1. se obtienen todos los registros de la DB
    medicamentos = db.query(model.Medicamento).all()
    lista_alertas = [] # lista que espera las alertas

    for m in medicamentos:
        # se convierte el texto "YYYY-MM-DD" a un objeto de fecha real
        fecha_venc = datetime.strptime(m.vencimiento, "%Y-%m-%d").date()
        dias_restantes = (fecha_venc - hoy).days
        
        # se hace el filtro si vence en menos de 60 días o ya venció
        
        if dias_restantes <= 60:
            
            # Clasificamos la gravedad
            if dias_restantes <= 30:
                status = "CRÍTICO/INMINENTE"
            elif dias_restantes < 10:
                status = "VENCIDO"
            else:
                status = "MANEJAR SEGUN POLITICA DE LAB"
            
            # Creamos el objeto de respuesta
            
            alerta = schema.AlertaMedicamento(
                id=m.id,
                nombre=m.nombre,
                lote=m.lote,
                laboratorio=m.laboratorio,
                vencimiento=m.vencimiento,
                dias_para_vencer=dias_restantes,
                estado=status
            )
            lista_alertas.append(alerta)
            
    return lista_alertas



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



def base_data():
    db = database.SessionLocal()
    try:
        # Solo poblamos la base si está totalmente vacía
        
        if db.query(model.Medicamento).count() == 0:
            productos = [
                # Medicamentos Reales y conocidos de varios laboratorios
                model.Medicamento(nombre="Amoxicilina 500mg", lote="L-101", laboratorio="Genfar", vencimiento="2025-11-15"),
                model.Medicamento(nombre="Losartán 50mg", lote="L-202", laboratorio="MK", vencimiento="2026-03-10"),
                model.Medicamento(nombre="Omeprazol 20mg", lote="L-303", laboratorio="Tecnoquímicas", vencimiento="2026-01-25"),
                model.Medicamento(nombre="Metformina 850mg", lote="L-404", laboratorio="La Santé", vencimiento="2026-05-15"),
                model.Medicamento(nombre="Atorvastatina 20mg", lote="L-505", laboratorio="Pfizer", vencimiento="2026-05-30"),
                model.Medicamento(nombre="Acetaminofén 500mg", lote="L-606", laboratorio="Genfar", vencimiento="2026-07-10"),
                model.Medicamento(nombre="Ibuprofeno 400mg", lote="L-707", laboratorio="MK", vencimiento="2026-07-28"),
                model.Medicamento(nombre="Loratadina 10mg", lote="L-808", laboratorio="Tecnoquímicas", vencimiento="2027-01-01"),
                model.Medicamento(nombre="Enalapril 20mg", lote="L-909", laboratorio="La Santé", vencimiento="2027-05-20"),
                model.Medicamento(nombre="Sertralina 50mg", lote="L-010", laboratorio="Pfizer", vencimiento="2025-10-20"),
                
                # Medicamentos Adicionales (Laboratorios Propios/Ficticios para variedad)
                model.Medicamento(nombre="Ciprofloxacino 500mg", lote="L-011", laboratorio="Bayer", vencimiento="2026-02-28"),
                model.Medicamento(nombre="Naproxeno 500mg", lote="L-012", laboratorio="FarmaGlobal", vencimiento="2026-12-15"),
                model.Medicamento(nombre="Azitromicina 500mg", lote="L-013", laboratorio="BioSalud S.A.", vencimiento="2026-04-10"),
                model.Medicamento(nombre="Vitamina C 1g", lote="L-014", laboratorio="NutriCorp", vencimiento="2027-08-20"),
                model.Medicamento(nombre="Dexametasona 4mg", lote="L-015", laboratorio="Hospira", vencimiento="2026-01-15"),
                model.Medicamento(nombre="Clotrimazol Crema", lote="L-016", laboratorio="Dermacare", vencimiento="2027-03-10"),
                model.Medicamento(nombre="Salbutamol Inhalador", lote="L-017", laboratorio="Glaxo", vencimiento="2026-09-05"),
                model.Medicamento(nombre="Glibenclamida 5mg", lote="L-018", laboratorio="MediCloud", vencimiento="2026-11-30"),
                model.Medicamento(nombre="Ranitidina 150mg", lote="L-019", laboratorio="Gastrolab", vencimiento="2025-12-01"),
                model.Medicamento(nombre="Captopril 25mg", lote="L-020", laboratorio="CardioFarma", vencimiento="2027-02-14")
            ]
            db.add_all(productos)
            db.commit()
            print("Base de datos cargada exitosamente con 20 productos.")
    except Exception as e:
        print(f"Error al cargar la base de datos: {e}")
    finally:
        db.close()

# llama a la funcion y ejecuta
base_data()

