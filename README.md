# ABM de Contactos (Tkinter + SQLite)

Aplicación simple para gestionar contactos (ABM: Alta, Baja, Modificación) usando Python, Tkinter para la interfaz de usuario y SQLite como base de datos embebida.

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
git clone https://github.com/tomivillarruelDev/ABM_Contactos.git
cd ABM_Contactos

# (opcional) entorno virtual
python -m venv .venv
source .venv/Scripts/activate
```

2. Dependencias: no hay dependencias externas.

3. Base de datos: ya se incluye `database/contactos.db`.

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

docs/                    # Documentación

gui/
	main_app.py            # Interfaz Tkinter

models/
	contacto.py            # Modelo de dominio Contacto

repository/
	contacto_repository.py # Capa CRUD

services/
	db_services.py         # Servicios DB/negocio

README.md
```

## Base de datos

- Ruta configurada en `config/settings.py`:

```
DB_PATH = "database/contactos.db"
```

- Esquema principal (`database/schema.sql`):