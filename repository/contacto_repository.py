from database.conexion import obtener_conexion, cerrar_conexion
from models.contacto import Contacto

class ContactoRepository:
    
    def agregar(self, contacto: Contacto):
        query = "INSERT INTO contactos (nombre, apellido, telefono, email) VALUES (?, ?, ?, ?)"
        conn = obtener_conexion()
        cursor = conn.cursor()
        valores = contacto.to_tuple()
        cursor.execute(query, valores)
        conn.commit()
        cerrar_conexion(conn)
