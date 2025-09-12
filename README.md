ESTRUCTURA:
/
│
├── config/
│   └── settings.py            # Parámetros de configuración (ej. DB_HOST, DB_NAME, etc.)
│
├── database/
│   ├── conexion.py            # Funciones para abrir/cerrar conexión
│   └── schema.sql             # Script de creación de la tabla
│
├── models/
│   └── contacto.py            # Clase Contacto (POO)
│
├── repository/
│   └── contacto_repository.py # CRUD de contactos usando la conexión
│
├── gui/
│   └── main_app.py            # Interfaz gráfica Tkinter
│
├── docs/
│   ├── diagrama_clases.png    
│   ├── modelo_datos.png       
│   └── informe.pdf            
│
└── README.md



settings.py → solo parámetros de configuración.

conexion.py → solo conexión.

repository → solo CRUD.

gui → solo interfaz.

models → solo clases.