
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import logging
import atexit
from app import vistas
from app.vistas import backup_y_limpiar_facturas_inventario_mensual, chequear_y_notificar_examenes_vencidos, create_tables_and_seed_data, limpiar_facturas_y_productos_eliminados_mensual, send_email
from conexion import engine, Base, get_db
import app.modelos as modelos
import app.schemas as schemas
from app.schemas import generate_history_html
from app.vistas import limpiar_tareas_completadas_mensual
from sqlalchemy.orm import Session
import os
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",           # desarrollo local
        "http://127.0.0.1:5173",
        "https://controlasbar.com",        # producción
        "https://www.controlasbar.com",    # por si usan www
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
if os.path.exists("app/static"):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(vistas.router)

def limpiar_historial_mensual():
    db: Session = next(get_db())
    try:
        bares = db.query(modelos.Bar).all()
        
        for bar in bares:
            if not bar.dueno or not bar.dueno.correo:
                continue

            historial = db.query(modelos.Historial).filter(modelos.Historial.bar_id == bar.id).all()
            if not historial:
                continue

            history_data = schemas.HistorialEmailData(
                bar_nombre=bar.nombre,
                fecha_borrado=datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                historial=[schemas.HistorialEmailItem.from_orm(item) for item in historial]
            )

            html = schemas.generate_history_html(history_data)
            send_email(
                to_email=bar.dueno.correo,
                subject=f"Backup mensual - Historial {bar.nombre} ({datetime.now().strftime('%B %Y')})",
                html_content=html
            )

            db.query(modelos.Historial).filter(modelos.Historial.bar_id == bar.id).delete(synchronize_session=False)
            db.commit()

            print(f"[{datetime.now()}] Historial enviado y borrado → {bar.nombre} (ID: {bar.id})")

    except Exception as e:
        db.rollback()
        print(f"Error en tarea automática: {e}")
    finally:
        db.close()

scheduler = BackgroundScheduler()

scheduler.add_job(
    func=limpiar_historial_mensual,
    trigger=CronTrigger(day=1, hour=3, minute=0),
    id='limpieza_mensual_historial',
    name='Backup mensual automático',
    replace_existing=True
)

scheduler.add_job(
    func=chequear_y_notificar_examenes_vencidos,
    trigger=CronTrigger(hour=2, minute=29),  # ← Todos los días a la 1:30 AM
    id='notificar_examenes_vencidos',
    name='Notificar exámenes médicos vencidos (una vez por vencimiento)',
    replace_existing=True
)
scheduler.add_job(
    func=limpiar_facturas_y_productos_eliminados_mensual,
    trigger=CronTrigger(day=1, hour=3, minute=5),  # Día 1 de cada mes a las 3:05 AM
    id='limpieza_mensual_facturas',
    name='Limpieza mensual automática de facturas y productos eliminados',
    replace_existing=True
)
scheduler.add_job(
    func=limpiar_tareas_completadas_mensual,
    trigger=CronTrigger(day=1, hour=3, minute=0),
    id='limpieza_mensual_tareas',
    name='Limpieza mensual de tareas + envío de correos',
    replace_existing=True
)
scheduler.add_job(
    func=backup_y_limpiar_facturas_inventario_mensual,
    trigger=CronTrigger(day=1, hour=3, minute=0),  # Día 1 de cada mes a las 3:00 AM
    id='backup_mensual_inventario',
    name='Backup mensual y limpieza de facturas de inventario',
    replace_existing=True
)
scheduler.start()
print("Verificando y creando tablas en la base de datos 'valka'...")
Base.metadata.create_all(bind=engine)
print("¡Todas las tablas están listas! (incluyendo las nuevas de inventario)")
create_tables_and_seed_data()
atexit.register(lambda: scheduler.shutdown(wait=False))