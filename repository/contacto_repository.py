from database.conexion import obtener_conexion, cerrar_conexion
from models.contacto import Contacto

class ContactoRepository:
    
    def agregar(self, contacto: Contacto):
        """ Agrega un nuevo contacto a la base de datos"""
        query = "INSERT INTO contactos (nombre, apellido, telefono, email) VALUES (?, ?, ?, ?)"
        conn = obtener_conexion()
        cursor = conn.cursor()
        valores = contacto.to_tuple()
        cursor.execute(query, valores)
        conn.commit()
        cerrar_conexion(conn)

    def obtener_por_id(self, contacto_id: int):
        """Obtiene un contacto por su ID. Retorna None si no existe."""
        query = "SELECT * FROM contactos WHERE id = ?"
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(query, (contacto_id,))
        row = cursor.fetchone()
        cerrar_conexion(conn)
        return Contacto.from_row(row) if row else None
    
    def actualizar(self, contacto: Contacto):
        """Actualiza un contacto existente"""
        if contacto.id is None:
            raise ValueError("El id del contacto es obligatorio para actualizar")

        existente = self.obtener_por_id(contacto.id)
        if not existente:
            # No existe el contacto a actualizar
            return False

        query = "UPDATE contactos SET nombre = ?, apellido = ?, telefono = ?, email = ? WHERE id = ?"
        conn = obtener_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute(query, contacto.to_tuple() + (contacto.id,))
            conn.commit()
            return True
        finally:
            cerrar_conexion(conn)
    
    def eliminar(self, contacto:Contacto):
        """Elimina un contacto existente"""
        if contacto.id is None:
            raise ValueError("El id del contacto es obligatorio para eliminar")
                
        query = "DELETE FROM contactos WHERE id=?"
        conn = obtener_conexion()
        try:
            cursor =conn.cursor()
            cursor.execute(query, (contacto.id,))
            conn.commit()
            return True
        finally:
            cerrar_conexion(conn)


