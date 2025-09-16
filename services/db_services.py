# services/db_services.py
from pathlib import Path
from database.conexion import obtener_conexion, cerrar_conexion

__all__ = ["init_schema"]  # Export explícito para evitar ambigüedades

def init_schema(schema_path: str = "database/schema.sql") -> None:

    #Ejecuta el DDL (CREATE TABLE IF NOT EXISTS ...) para que la tabla exista.

    conn = obtener_conexion()
    try:
        sql = Path(schema_path).read_text(encoding="utf-8")
        conn.executescript(sql)
        conn.commit()
    finally:
        cerrar_conexion(conn)
