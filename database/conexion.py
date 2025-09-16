import sqlite3
from config.settings import DB_PATH

def obtener_conexion():
    # abre una conexión SQLlite hacia la ruta DB_PATG
    try:
        #sqlite3.connect: conexión abierta a la base SQLite.
        conexion = sqlite3.connect(DB_PATH)
        return conexion
    except sqlite3.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None

def cerrar_conexion(conexion):
    #cierra la conexión si está abiera
    if conexion:
        conexion.close()
