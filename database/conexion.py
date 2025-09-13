import sqlite3
from config.settings import DB_PATH

def obtener_conexion():
    try:
        conexion = sqlite3.connect(DB_PATH)
        return conexion
    except sqlite3.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None

def cerrar_conexion(conexion):
    if conexion:
        conexion.close()



#a,e,i,o,u