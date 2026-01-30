# InventApp: Sistema de Gestión Farmacéutica Pro  

InventApp es una API REST de alto rendimiento desarrollada con FastAPI para el control inteligente de inventarios farmacéuticos. Este proyecto no solo gestiona datos, sino que implementa un motor de toma de decisiones para la seguridad sanitaria y la eficiencia operativa.  

Motor de Alertas Inteligente, equipado con  endpoint de alertas, que utiliza filtrado avanzado en SQL (vía SQLAlchemy) para procesar grandes volúmenes de datos directamente en el motor de base de datos, optimizando el consumo de memoria RAM.

Lógica de Clasificación de Inventario:El sistema categoriza automáticamente cada producto según su urgencia:

VENCIDO REPORTAR Y DESTRUIR: Productos con fecha pasada (Días < 0).  

"CRÍTICO / RETIRO INMINENTE: Vencimiento entre 0 y 35 días.

ALERTA / PRÓXIMOS 1-2 MESES: Vencimiento entre 36 y 65 días.  

POLÍTICA DE DEVOLUCIÓN: Margen de 66 a 180 días para gestión con proveedores.

Stack Tecnológico FastAPI: Framework de alto rendimiento.

SQLAlchemy (ORM): Consultas optimizadas y tipado fuerte.

SQLite: Persistencia de datos eficiente y portable.

Pydantic: Validación estricta de esquemas de datos.  

Estructura del Proyecto:  

TodoInvent/
├── database.py    # Configuración del Engine y Session de SQLAlchemy.
├── model.py       # Definición de la entidad 'Medicamento' (ORM).
├── schemas.py     # Modelos de validación y Esquemas de Reporte (Pydantic).
├── main.py        # Endpoints, lógica de negocio y Seed de datos.
└── farmacia_pro.db # Base de datos autogenerada.

Endpoints de la APIGestión de Inventario  

GET/medicamentos Obtiene el inventario completo.
GET/medicamentos/{id}Búsqueda precisa por ID.
GET/medicamentos/nombre/{nombre}Filtro por coincidencia de nombre.
GET/medicamentos/laboratorio/{lab}Filtro por fabricante.

Inteligencia de Negocio  

GET/medicamentos/alertas  
Reporte Ejecutivo: Totales de vencidos y lista clasificada.
GET/medicamentos/orden/vencimiento

Instalación Rápida

Instalar dependencias:

pip install fastapi uvicorn sqlalchemy

Iniciar servidor:

uvicorn main:app --reload  

pip install fastapi uvicorn sqlalchemy  
