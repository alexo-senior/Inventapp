InventApp Sistema de Gestión Farmacéutica

InventApp es una API REST profesional desarrollada con FastAPI para el control de inventarios farmacéuticos. El proyecto destaca por su arquitectura modular, manejo de errores robusto y automatización de alertas de vencimiento.

Características Principales

Arquitectura Modular:Separación de responsabilidades en capas (Models, Schemas, Database, Main).
ORM SQLAlchemy: Gestión de base de datos SQLite sin escribir SQL manual.
Validación con Pydantic: Esquemas de datos estrictos para garantizar la integridad de la información.
Documentación Automática: Swagger UI interactiva generada nativamente.
Seed Automático: Carga inicial de 20 productos para pruebas inmediatas.

Estructura del Proyecto
TodoInvent/
├── database.py   # Configuración y conexión del motor SQLAlchemy.
├── model.py      # Definición de tablas de la base de datos (Clases ORM).
├── schemas.py    # Modelos de Pydantic para validación y respuesta.
├── main.py       # Lógica central, endpoints y carga de datos iniciales.
└── farmacia_pro.db # Base de datos SQLite (generada automáticamente)

Instalar dependencias:

1.pip install fastapi uvicorn sqlalchemy

Ejecutar el servidor:
cd TodoInvent
uvicorn main:app --reload

Acceder a la documentación:
Abre <http://127.0.0.1:8000/docs> para probar los endpoints.
🛣️ Endpoints Disponibles
Método
Ruta
Descripción
GET
/medicamentos
Lista el inventario completo (20 productos).
GET
/medicamentos/id/{id}
Busca un producto por su ID único.
GET
/medicamentos/nombre/{nombre}
Filtra productos por coincidencia de nombre.
GET
/medicamentos/laboratorio/{lab}
Filtra productos por casa farmacéutica.
GET
/medicamentos/orden/vencimiento
Lista productos ordenados por fecha de caducidad.

.
