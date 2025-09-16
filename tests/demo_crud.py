import os
import sys
import sqlite3

# Asegurar que la carpeta raíz del proyecto esté en sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from models.contacto import Contacto
from repository.contacto_repository import ContactoRepository
from config.settings import DB_PATH


def contar_contactos() -> int:
    p = os.path.abspath(DB_PATH)
    conn = sqlite3.connect(p)
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM contactos")
        return cur.fetchone()[0]
    finally:
        conn.close()


def main():
    repo = ContactoRepository()
    print("Base de datos:", os.path.abspath(DB_PATH))

    total_inicial = contar_contactos()
    print("Total inicial:", total_inicial)

    # 1) Insertar
    contacto = Contacto(nombre="Demo", apellido="CRUD", telefono="1234567", email="demo@crud.com")
    repo.agregar(contacto)
    total_post_insert = contar_contactos()
    print("Total tras insertar:", total_post_insert)

    # Obtener el recién insertado (el de mayor id)
    todos = repo.obtener_todos()
    nuevo = max(todos, key=lambda c: c.id)
    print("Insertado:", nuevo)

    # 2) Actualizar
    nuevo.telefono = "7654321"
    actualizado = repo.actualizar(nuevo)
    print("Actualización aplicada:", actualizado)
    verificado = repo.obtener_por_id(nuevo.id)
    print("Teléfono actualizado:", verificado.telefono)

    # 3) Eliminar
    eliminado = repo.eliminar(verificado)
    print("Eliminado:", eliminado)
    total_final = contar_contactos()
    print("Total final:", total_final)


if __name__ == "__main__":
    main()
