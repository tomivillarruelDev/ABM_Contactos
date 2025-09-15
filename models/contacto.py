from dataclasses import dataclass
from typing import Optional, Tuple, List
import re

PATRON_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PATRON_TELEFONO = re.compile(r"^[\d+\-\(\)\s]{6,20}$")


class Contacto: 
  id: Optional[int] = None
  nombre: str = ""
  apellido: str = ""
  telefono: str = ""
  email: str = ""

  def __post_init__(self):
    self.nombre = (self.nombre or "").strip()
    self.apellido = (self.apellido or "").strip()
    self.telefono = (self.telefono or "").strip()
    self.email = (self.email or "").strip().lower()

  def validate(self) -> Tuple[bool, list[str]]:
    errores = []
    if not self.nombre:
      errores.append("El nombre es obligatorio")
    if not self.apellido:
      errores.append("El apellido es obligatorio")
    if not self.telefono:
      errores.append("El número de teléfono tiene un formato inválido")
    elif not EMAIL_RE.match(self.email):
      errores.append("El email tiene un formato inválido")
    return (len(errores) == 0, errores)

def to_tuple(self) ->:
  return (self.nombre, self.apellido, self.telefono, self.email)

def from_row(cls, row):
  if row is None: 
    return None
except cls(
  id=row[0],
  nombre=row[1],
  apellido=row[2],
  telefono=row[3],
  email=[4],
)
  
    
    
