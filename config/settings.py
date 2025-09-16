# config/settings.py
from pathlib import Path

# BASE_DIR apunta a la carpeta raíz del proyecto (donde están /gui, /repository, /database, etc.)
BASE_DIR = Path(__file__).resolve().parents[1]

# Ruta ABSOLUTA a la base, para no depender del directorio de ejecución
DB_PATH = (BASE_DIR / "database" / "contactos.db").as_posix()