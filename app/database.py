import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if SQLALCHEMY_DATABASE_URL:
    # 1. Normalizar el esquema de la URL
    if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
    elif SQLALCHEMY_DATABASE_URL.startswith("postgresql://"):
        SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
    
    # 2. Si la URL es externa (no contiene 'render.com' interno), forzar SSL
    # Esto es solo por si acaso, pero en Render deberías usar la Internal URL
    if "sslmode" not in SQLALCHEMY_DATABASE_URL and "render.com" in SQLALCHEMY_DATABASE_URL:
        # Solo añadir SSL si es una URL externa (la interna no lo necesita)
        if "dpg-" in SQLALCHEMY_DATABASE_URL and "oregon-postgres.render.com" in SQLALCHEMY_DATABASE_URL:
             pass # La URL interna usa el mismo host, así que no podemos distinguir fácilmente.
             # Lo dejamos así porque NullPool debería ser suficiente.
else:
    SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://libreria_user:libreria_pass@localhost:5432/libreria_db"

# --- LA CLAVE: NullPool elimina el problema de conexiones muertas ---
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=NullPool,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()