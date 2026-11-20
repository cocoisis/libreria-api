from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from . import models, database, auth, schemas
from .routers import libros, editoriales

# Crear las tablas al iniciar (para desarrollo)
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Librería Chiapas API",
    description="API REST para la administración de libros y editoriales",
    version="1.0.0",
)

# Incluir routers
app.include_router(libros.router)
app.include_router(editoriales.router)


@app.post("/login", response_model=schemas.Token, tags=["Autenticación"])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = db.query(models.Usuario).filter(models.Usuario.nomuser == form_data.username).first()

    if not user or not auth.verify_password(form_data.password, user.passwd):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.nomuser}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/healthz", include_in_schema=False)
def health():
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
def root():
    return {"mensaje": "Bienvenido a la API de Librería Chiapas. Ve a /docs para la documentación."}