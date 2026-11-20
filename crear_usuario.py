from app.auth import get_password_hash
from app import database, models
from app.database import SessionLocal

# Crear tablas si no existen
models.Base.metadata.create_all(bind=database.engine)

# Abrir sesión
db = SessionLocal()

# Verificar si el usuario ya existe para no duplicarlo
usuario_existente = db.query(models.Usuario).filter(
    models.Usuario.nomuser == "admin"
).first()

if usuario_existente:
    print("⚠️  El usuario 'admin' ya existe. No se creó de nuevo.")
else:
    usuario = models.Usuario(
        nomuser="admin",
        passwd=get_password_hash("admin123"),
        nombrecompleto="Administrador Librería Chiapas"
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    print(f"✅ Usuario creado correctamente: id={usuario.id}, nomuser={usuario.nomuser}")

db.close()