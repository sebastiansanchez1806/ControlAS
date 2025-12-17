

import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Detectamos automáticamente si estamos en local o producción
if os.path.exists("/var/www"):  # En el servidor
    SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://controlasbar:1806@localhost/controlasbar"
    extra_args = {}
else:  # En tu PC (local)
    SQLALCHEMY_DATABASE_URL = "sqlite:///./controlasbar_local.db"
    extra_args = {"connect_args": {"check_same_thread": False}}

engine = create_engine(SQLALCHEMY_DATABASE_URL, **extra_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()