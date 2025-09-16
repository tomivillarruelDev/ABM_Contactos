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

    def obtener_todos(self):
        """Obtiene todos los contactos de la base de datos."""
        query = "SELECT * FROM contactos"
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cerrar_conexion(conn)
        return [Contacto.from_row(row) for row in rows]
    
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
        """Actualiza un contacto existente de forma dinámica.
        
        Solo actualiza los campos que son diferentes del contacto existente.
        """
        if contacto.id is None:
            raise ValueError("El id del contacto es obligatorio para actualizar")

        existente = self.obtener_por_id(contacto.id)
        if not existente:
            return False

        # Construir dinámicamente la consulta SQL
        campos_actualizar = []
        valores = []
        
        # Solo actualizar campos que son diferentes y no están vacíos
        if (contacto.nombre is not None and contacto.nombre != "" and 
            contacto.nombre != existente.nombre):
            campos_actualizar.append("nombre = ?")
            valores.append(contacto.nombre)
        
        if (contacto.apellido is not None and contacto.apellido != "" and 
            contacto.apellido != existente.apellido):
            campos_actualizar.append("apellido = ?")
            valores.append(contacto.apellido)
        
        if (contacto.telefono is not None and contacto.telefono != "" and 
            contacto.telefono != existente.telefono):
            campos_actualizar.append("telefono = ?")
            valores.append(contacto.telefono)
        
        if (contacto.email is not None and contacto.email != "" and 
            contacto.email != existente.email):
            campos_actualizar.append("email = ?")
            valores.append(contacto.email)

        # Si no hay campos para actualizar, retornar False
        if not campos_actualizar:
            return False

        # Construir la consulta SQL
        query = f"UPDATE contactos SET {', '.join(campos_actualizar)} WHERE id = ?"
        valores.append(contacto.id)

        conn = obtener_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute(query, valores)
            conn.commit()
            return cursor.rowcount > 0
        finally:
            cerrar_conexion(conn)
            
    def eliminar(self, contacto:Contacto):
        """Elimina un contacto existente"""
        if contacto.id is None:
            raise ValueError("El id del contacto es obligatorio para eliminar")
                
        query = "DELETE FROM contactos WHERE id=?"
        conn = obtener_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (contacto.id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            cerrar_conexion(conn)