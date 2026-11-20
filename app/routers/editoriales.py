from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database
from ..auth import get_current_user

router = APIRouter(prefix="/editoriales", tags=["Editoriales"])


# ---------- CRUD ----------
@router.get("/", response_model=List[schemas.EditorialResponse])
def listar_editoriales(db: Session = Depends(database.get_db)):
    return db.query(models.Editorial).all()


@router.get("/{editorial_id}", response_model=schemas.EditorialResponse)
def obtener_editorial(editorial_id: int, db: Session = Depends(database.get_db)):
    editorial = db.query(models.Editorial).filter(models.Editorial.id == editorial_id).first()
    if not editorial:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")
    return editorial


@router.post(
    "/",
    response_model=schemas.EditorialResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
def crear_editorial(editorial: schemas.EditorialCreate, db: Session = Depends(database.get_db)):
    nueva = models.Editorial(**editorial.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@router.put(
    "/{editorial_id}",
    response_model=schemas.EditorialResponse,
    dependencies=[Depends(get_current_user)],
)
def actualizar_editorial(
    editorial_id: int,
    editorial: schemas.EditorialCreate,
    db: Session = Depends(database.get_db),
):
    db_edit = db.query(models.Editorial).filter(models.Editorial.id == editorial_id).first()
    if not db_edit:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")

    for key, value in editorial.model_dump().items():
        setattr(db_edit, key, value)

    db.commit()
    db.refresh(db_edit)
    return db_edit


@router.delete("/{editorial_id}", dependencies=[Depends(get_current_user)])
def eliminar_editorial(editorial_id: int, db: Session = Depends(database.get_db)):
    editorial = db.query(models.Editorial).filter(models.Editorial.id == editorial_id).first()
    if not editorial:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")

    db.delete(editorial)
    db.commit()
    return {"mensaje": f"Editorial con id {editorial_id} eliminada correctamente"}