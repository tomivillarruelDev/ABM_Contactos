# ABM de Contactos (Tkinter + SQLite)

Aplicación simple para gestionar contactos (ABM: Alta, Baja, Modificación) usando Python, Tkinter para la interfaz de usuario y SQLite como base de datos embebida.

## Estado actual

- La app GUI abre una ventana de ejemplo con Tkinter (`gui/main_app.py`).
- La base de datos SQLite y el esquema existen (`database/contactos.db` y `database/schema.sql`).
- Pendiente de implementación: `models/contacto.py`, `services/db_services.py` y la lógica CRUD completa en `repository/contacto_repository.py`.

## Tecnologías

- Python 3.10+ (estándar de biblioteca)
- Tkinter (incluido con Python)
- SQLite (incluido con Python vía `sqlite3`)

## Requisitos previos

- Windows con Python 3 instalado y agregado al PATH.

## Instalación y ejecución rápida

1. Clonar el repositorio y (opcional) crear un entorno virtual:

```bash
# clonar
git clone https://github.com/tomivillarruelDev/ABM_Contactos-.git
cd ABM_Contactos-

# (opcional) entorno virtual
python -m venv .venv
source .venv/Scripts/activate
```

2. Dependencias: no hay dependencias externas (Tkinter y sqlite3 vienen con Python).

3. Base de datos: ya se incluye `database/contactos.db`. Si querés recrearla desde cero:

```bash
python - << 'PY'
import sqlite3, pathlib
db = pathlib.Path('database/contactos.db')
sql = pathlib.Path('database/schema.sql').read_text(encoding='utf-8')
db.parent.mkdir(parents=True, exist_ok=True)
con = sqlite3.connect(db.as_posix())
con.executescript(sql)
con.commit(); con.close()
print('Base recreada en', db)
PY
```

4. Ejecutar la aplicación (demo Tkinter por ahora):

```bash
python gui/main_app.py
```

## Estructura del proyecto

```
config/
	settings.py            # Parámetros de configuración (DB_PATH)

database/
	conexion.py            # Abrir/cerrar conexión SQLite
	contactos.db           # Base de datos (incluida)
	schema.sql             # Script SQL para crear tabla(s)
	init/                  # (reservado para seeds/migraciones)

docs/                    # Documentación (vacío por ahora)

gui/
	main_app.py            # Interfaz Tkinter (demo actual)

models/
	contacto.py            # Modelo de dominio Contacto (pendiente)

repository/
	contacto_repository.py # Capa CRUD (a completar)

services/
	db_services.py         # Servicios DB/negocio (pendiente)

README.md
```

## Base de datos

- Ruta configurada en `config/settings.py`:

```
DB_PATH = "database/contactos.db"
```

- Esquema principal (`database/schema.sql`):

```sql
CREATE TABLE contactos (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		nombre TEXT NOT NULL,
		apellido TEXT NOT NULL,
		telefono TEXT NOT NULL,
		email TEXT NOT NULL
);
```

## Próximos pasos (TODO)

- Implementar `models/Contacto` con validaciones básicas.
- Completar `repository/contacto_repository.py` con operaciones CRUD usando `database/conexion.py`.
- Crear `services/db_services.py` para encapsular lógica de negocio (ej. validación, formateo, duplicados).
- Conectar la GUI a los servicios para alta/edición/borrado/listado de contactos.
- Agregar tests mínimos (unittest/pytest) y documentación en `docs/`.

## Solución de problemas

- Error al abrir DB: asegurate de ejecutar los comandos desde la raíz del repo para que la ruta relativa `database/contactos.db` sea válida.
- Tkinter no abre: verificá que estés usando el Python oficial (no minimal) y que `python -m tkinter` funcione.

## Licencia

No se especificó una licencia. Si corresponde, agregá un archivo LICENSE.

ESTRUCTURA:
/
│
├── config/
│ └── settings.py # Parámetros de configuración (ej. DB_HOST, DB_NAME, etc.)
│
├── database/
│ ├── conexion.py # Funciones para abrir/cerrar conexión
│ └── schema.sql # Script de creación de la tabla
│
├── models/
│ └── contacto.py # Clase Contacto (POO)
│
├── repository/
│ └── contacto_repository.py # CRUD de contactos usando la conexión
│
├── gui/
│ └── main_app.py # Interfaz gráfica Tkinter
│
├── docs/
│ ├── diagrama_clases.png  
│ ├── modelo_datos.png  
│ └── informe.pdf  
│
└── README.md

settings.py → solo parámetros de configuración.

conexion.py → solo conexión.

repository → solo CRUD.

gui → solo interfaz.

models → solo clases.
