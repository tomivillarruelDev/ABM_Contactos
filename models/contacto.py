from dataclasses import dataclass
from typing import Optional, Tuple, List
import re

PATRON_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PATRON_TELEFONO = re.compile(r"^[\d+\-\(\)\s]{6,20}$")

@dataclass
class Contacto:
  id: Optional[int] = None
  nombre: str = ""
  apellido: str = ""
  telefono: str = ""
  email: str = ""

  def __post_init__(self):
    """Limpia y normaliza los datos después de la inicialización"""
    self.nombre = (self.nombre or "").strip()
    self.apellido = (self.apellido or "").strip()
    self.telefono = (self.telefono or "").strip()
    self.email = (self.email or "").strip().lower()

  def validate(self) -> Tuple[bool, List[str]]:
    """Valida los datos del contacto. Retorna una tupla (es_valido, lista_de_errores)"""
    errores: List[str] = []
    if not self.nombre:
      errores.append("El nombre es obligatorio")
    if not self.apellido:
      errores.append("El apellido es obligatorio")
    if not self.telefono:
      errores.append("El teléfono es obligatorio")
    elif not PATRON_TELEFONO.match(self.telefono):
      errores.append("El número de teléfono tiene un formato inválido")
    if not self.email:
      errores.append("El email es obligatorio")
    elif not PATRON_EMAIL.match(self.email):
      errores.append("El email tiene un formato inválido")
    return (len(errores) == 0, errores)

  def to_tuple(self) -> Tuple[str, str, str, str]:
    """Convierte el contacto a una tupla para operaciones en la BD"""
    return (self.nombre, self.apellido, self.telefono, self.email)

  @classmethod
  def from_row(cls, row: tuple):
    """Crea un objeto Contacto desde una fila de la BD"""
    if row is None:
      return None
    return cls(
      id=row[0],
      nombre=row[1],
      apellido=row[2],
      telefono=row[3],
      email=row[4],
    )