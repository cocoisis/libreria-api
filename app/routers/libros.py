from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database
from ..auth import get_current_user

router = APIRouter(prefix="/libros", tags=["Libros"])


# ---------- Consultas personalizadas (van ANTES de /{id}) ----------
@router.get("/sinexistencia", response_model=List[schemas.LibroResponse])
def libros_sin_existencia(db: Session = Depends(database.get_db)):
    return db.query(models.Libro).filter(models.Libro.existencia == 0).all()


@router.get("/editorial/{editorial_id}", response_model=List[schemas.LibroResponse])
def libros_por_editorial(editorial_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Libro).filter(models.Libro.editorial_id == editorial_id).all()


@router.get("/anio/{anio}", response_model=List[schemas.LibroResponse])
def libros_por_anio(anio: int, db: Session = Depends(database.get_db)):
    return db.query(models.Libro).filter(models.Libro.anio == anio).all()


# ---------- CRUD ----------
@router.get("/", response_model=List[schemas.LibroResponse])
def listar_libros(db: Session = Depends(database.get_db)):
    return db.query(models.Libro).all()


@router.get("/{libro_id}", response_model=schemas.LibroResponse)
def obtener_libro(libro_id: int, db: Session = Depends(database.get_db)):
    libro = db.query(models.Libro).filter(models.Libro.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro


@router.post(
    "/",
    response_model=schemas.LibroResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
def crear_libro(libro: schemas.LibroCreate, db: Session = Depends(database.get_db)):
    # Validar que la editorial exista
    editorial = db.query(models.Editorial).filter(models.Editorial.id == libro.editorial_id).first()
    if not editorial:
        raise HTTPException(status_code=400, detail="La editorial indicada no existe")

    nuevo = models.Libro(**libro.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.put(
    "/{libro_id}",
    response_model=schemas.LibroResponse,
    dependencies=[Depends(get_current_user)],
)
def actualizar_libro(
    libro_id: int,
    libro: schemas.LibroCreate,
    db: Session = Depends(database.get_db),
):
    db_libro = db.query(models.Libro).filter(models.Libro.id == libro_id).first()
    if not db_libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    for key, value in libro.model_dump().items():
        setattr(db_libro, key, value)

    db.commit()
    db.refresh(db_libro)
    return db_libro


@router.delete("/{libro_id}", dependencies=[Depends(get_current_user)])
def eliminar_libro(libro_id: int, db: Session = Depends(database.get_db)):
    libro = db.query(models.Libro).filter(models.Libro.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    db.delete(libro)
    db.commit()
    return {"mensaje": f"Libro con id {libro_id} eliminado correctamente"}