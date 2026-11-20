from pydantic import BaseModel, EmailStr
from typing import List


# ---------- Editorial ----------
class EditorialBase(BaseModel):
    nombre: str
    pais: str
    email: EmailStr


class EditorialCreate(EditorialBase):
    pass


class EditorialResponse(EditorialBase):
    id: int

    class Config:
        from_attributes = True


# ---------- Libro ----------
class LibroBase(BaseModel):
    titulo: str
    autor: str
    isbn: str
    anio: int
    existencia: int
    editorial_id: int


class LibroCreate(LibroBase):
    pass


class LibroResponse(LibroBase):
    id: int

    class Config:
        from_attributes = True


# ---------- Usuario ----------
class UsuarioBase(BaseModel):
    nomuser: str
    nombrecompleto: str


class UsuarioCreate(UsuarioBase):
    passwd: str


class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True


# ---------- Token ----------
class Token(BaseModel):
    access_token: str
    token_type: str