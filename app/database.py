from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# En local usa tus credenciales de PostgreSQL; en Render usa la variable de entorno DATABASE_URL
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://libreria_user:libreria_pass@localhost:5432/libreria_db"
)

# Render a veces entrega "postgres://", SQLAlchemy necesita "postgresql://"
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()