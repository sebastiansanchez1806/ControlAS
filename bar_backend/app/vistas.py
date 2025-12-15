
import calendar
from datetime import date, datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from multiprocessing import get_context
import os
import pytz
import secrets
from passlib.context import CryptContext
from app.correo import enviar_email_tarea
from app.send_email import send_email 
import smtplib
from sqlite3 import IntegrityError
from typing import Dict, List, Optional
from fastapi import APIRouter, File, Form, Query, UploadFile
from sqlalchemy import desc, func
from sqlalchemy.exc import OperationalError
from app import schemas
from app import modelos
from conexion import engine
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from conexion import get_db
from app.modelos import Administrador, Bar, DetalleFactura, DetalleFacturaInventario, Dueno, Factura, FacturaInventario, Gasto, GestorPrincipal, Historial, Mujer, NotificacionExamenEnviada, Producto, ProductoEliminado, Tarea
from app.schemas import ActualizarCantidad, AdministradorCreate, AdministradorOut, AdministradorUpdate, BarCreate, BarOut, BarUpdate, DetalleFacturaOut, DuenoCreate, DuenoOut, DuenoUpdate, FacturaData, ForgotPasswordRequest, GestorPrincipalLoginRequest, GestorPrincipalLoginResponse, GestorPrincipalOut, GestorPrincipalPasswordUpdate, GestorPrincipalUpdate, HistorialOut, HistorialSimpleOut, HistorialWithProduct, LoginRequest, LoginResponse, MujerCreate, MujerOut, MujerUpdate, ProductoCreate, ProductoInfo, ProductoOut, ProductoUpdate, ResetPasswordRequest, TareaCreate, TareaOut, generate_invoice_html, get_password_hash
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
@router.on_event("startup")
def verificar_conexion():
    try:
        with engine.connect() as conn:
            print("✅ Conexión exitosa a la base de datos.")
    except OperationalError as e:
        print("❌ Error de conexión:", e)
        raise RuntimeError("❌ No se pudo conectar a la base de datos.")

@router.post("/duenos", response_model=DuenoOut, status_code=status.HTTP_201_CREATED)
def crear_dueno(dueno: DuenoCreate, db: Session = Depends(get_db)):
    # Validar correo único
    if db.query(modelos.Dueno).filter(modelos.Dueno.correo == dueno.correo).first():
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    # Validar nombre único
    if db.query(modelos.Dueno).filter(modelos.Dueno.nombre == dueno.nombre).first():
        raise HTTPException(status_code=400, detail="Ya existe un dueño con ese nombre")

    hashed_password = pwd_context.hash(dueno.contraseña)
    nuevo_dueno = modelos.Dueno(
        nombre=dueno.nombre,
        correo=dueno.correo,
        contraseña=hashed_password,
        imagen=dueno.imagen,
        estado=dueno.estado or "activo",
        telefono=dueno.telefono,
        cantidad_bares=dueno.cantidad_bares  # ← AGREGADO
    )
    db.add(nuevo_dueno)
    db.commit()
    db.refresh(nuevo_dueno)
    return nuevo_dueno

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # 🔹 Lógica de login para Dueño (sin bar_id)
    if request.bar_id is None:
        dueno = db.query(Dueno).filter(Dueno.nombre == request.nombre).first()
        if not dueno:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Verificar si la cuenta está inactiva
        if dueno.estado == "inactivo":
            raise HTTPException(
                status_code=403,  # 403 Forbidden es perfecto para cuentas bloqueadas
                detail="Tu cuenta está bloqueada por falta de pago. Por favor, comunícate con servicio al cliente para reactivarla."
            )

        # Verificar contraseña
        if not pwd_context.verify(request.contraseña, dueno.contraseña):
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")

        # Login exitoso
        return LoginResponse(
            id=dueno.id,
            nombre=dueno.nombre,
            correo=dueno.correo,
            tipo="dueno",
            telefono=dueno.telefono,
            imagen=dueno.imagen,
            foto=None,
            bar_id=None,
            dueno_id=None,
            bar_nombre=None
        )

    # 🔹 Lógica de login para Administrador (con bar_id)
    else:
        administrador = db.query(Administrador).filter(
            Administrador.nombre == request.nombre,
            Administrador.bar_id == request.bar_id
        ).first()
        
        if not administrador:
            raise HTTPException(
                status_code=404, 
                detail="Administrador no encontrado en este bar o credenciales incorrectas"
            )

        if not pwd_context.verify(request.contraseña, administrador.contraseña):
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")

        bar = db.query(Bar).filter(Bar.id == administrador.bar_id).first()
        bar_nombre = bar.nombre if bar else None
        dueno_id = bar.dueno_id if bar else None

        return LoginResponse(
            id=administrador.id,
            nombre=administrador.nombre,
            correo=administrador.correo,
            tipo="administrador",
            telefono=administrador.telefono,
            imagen=None,
            foto=administrador.foto,
            bar_id=administrador.bar_id,
            dueno_id=dueno_id,
            bar_nombre=bar_nombre
        )
# endpoint corregido:

@router.get("/bares/dueno/{dueno_id}", response_model=dict)
def obtener_bares_por_dueno(dueno_id: int, db: Session = Depends(get_db)):
    bares = db.query(Bar).filter(Bar.dueno_id == dueno_id).all()
    
    if not bares:
        return {"mensaje": "Este dueño no tiene bares registrados", "bares": []}

    lista_bares = [
        {
            "id": bar.id,
            "nombre": bar.nombre,
            "ubicacion": bar.ubicacion,

            "dueno_id": bar.dueno_id,
            # ✨ AGREGAR EL CAMPO TIPO AQUÍ ✨
            "tipo": bar.tipo, 
            "imagen": bar.imagen,
        } 
        for bar in bares
    ]

    return {
        "mensaje": "Bares encontrados exitosamente",
        "bares": lista_bares
    }
@router.post("/crea_bares", response_model=dict)
def crear_bar(bar: BarCreate, db: Session = Depends(get_db)):

    nuevo_bar = Bar(
        nombre=bar.nombre,
        ubicacion=bar.ubicacion,
        imagen=bar.imagen,
        dueno_id=bar.dueno_id,
        # 🌟 Campo 'tipo' usado correctamente
        tipo=bar.tipo 
    )
    
    db.add(nuevo_bar)
    db.commit()
    db.refresh(nuevo_bar)
    
    return {
        "mensaje": "Bar creado exitosamente",
        "bar": {
            "id": nuevo_bar.id,
            "nombre": nuevo_bar.nombre,
            "ubicacion": nuevo_bar.ubicacion,
            "imagen": nuevo_bar.imagen,
            "dueno_id": nuevo_bar.dueno_id,
            # 🌟 Retorna el tipo de local
            "tipo_local": nuevo_bar.tipo  # Lo renombramos a tipo_local para que coincida con Vue (opcional, pero útil)
        }
    }
@router.get("/dueno/{dueno_id}/info")
def info_dueno(dueno_id: int, db: Session = Depends(get_db)):
    dueno = db.query(Dueno).filter(Dueno.id == dueno_id).first()
    if not dueno:
        raise HTTPException(status_code=404, detail="Dueño no encontrado")
    
    bares_count = db.query(Bar).filter(Bar.dueno_id == dueno_id).count()

    return {
        "cantidad_permitida": dueno.cantidad_bares,
        "cantidad_actual": bares_count,
        "puede_crear_mas": bares_count < dueno.cantidad_bares
    }
@router.delete("/bares_eliminar/{bar_id}", response_model=dict)
def eliminar_bar(bar_id: int, db: Session = Depends(get_db)):
    bar = db.query(Bar).filter(Bar.id == bar_id).first()
    
    if not bar:
        raise HTTPException(status_code=404, detail="Bar no encontrado")

    nombre_bar = bar.nombre
    
    try:
        # ✅ PASO 1: Eliminar manualmente las facturas de inventario asociadas
        # Primero eliminar los detalles de las facturas
        facturas_inventario = db.query(FacturaInventario).filter(
            FacturaInventario.bar_id == bar_id
        ).all()
        
        for factura_inv in facturas_inventario:
            # Eliminar los detalles de cada factura de inventario
            db.query(DetalleFacturaInventario).filter(
                DetalleFacturaInventario.factura_inventario_id == factura_inv.id
            ).delete()
        
        # Luego eliminar las facturas de inventario
        db.query(FacturaInventario).filter(
            FacturaInventario.bar_id == bar_id
        ).delete()
        
        # ✅ PASO 2: Ahora eliminar el bar (esto eliminará automáticamente 
        # todo lo que SÍ tiene cascade: administradores, productos, historial, etc.)
        db.delete(bar)
        
        db.commit()
        return {"mensaje": f"Bar '{nombre_bar}' y todos sus registros relacionados eliminados exitosamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar: {str(e)}")
@router.put("/bares_actualizar/{bar_id}", response_model=dict)
def editar_bar(bar_id: int, datos_bar: BarUpdate, db: Session = Depends(get_db)):
    bar = db.query(Bar).filter(Bar.id == bar_id).first()
    if not bar:
        raise HTTPException(status_code=404, detail="No se encontró un bar con ese ID")

    if datos_bar.nombre is not None:
        bar.nombre = datos_bar.nombre

    if datos_bar.ubicacion is not None:
        bar.ubicacion = datos_bar.ubicacion

    if datos_bar.imagen is not None:
        bar.imagen = datos_bar.imagen
    db.commit()
    db.refresh(bar)

    return {
        "mensaje": "Bar actualizado exitosamente",
        "bar": {
            "id": bar.id,
            "nombre": bar.nombre,
            "ubicacion": bar.ubicacion,
            "imagen": bar.imagen,
            "dueno_id": bar.dueno_id
        }
    }
    


@router.post("/mujeres", response_model=MujerOut)
def crear_mujer(mujer: MujerCreate, db: Session = Depends(get_db)):
    # Validación extra por si alguien intenta saltarse el frontend
    if not mujer.fecha_examen:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha del examen médico es obligatoria"
        )
    if not mujer.foto_examen or len(mujer.foto_examen) < 50:  # base64 muy corto = inválido
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes subir la foto o PDF del examen médico"
        )

    nueva_mujer = Mujer(**mujer.dict())
    db.add(nueva_mujer)
    db.commit()
    db.refresh(nueva_mujer)
    return nueva_mujer  
@router.delete("/mujeres_eliminar/{mujer_id}", response_model=dict)
def eliminar_mujer(mujer_id: int, db: Session = Depends(get_db)):
    mujer = db.query(Mujer).filter(Mujer.id == mujer_id).first()
    if not mujer:
        raise HTTPException(status_code=404, detail="Mujer no encontrada")
    db.delete(mujer)
    db.commit()
    return {"mensaje": "Mujer eliminada correctamente"}

@router.put("/mujeres/{mujer_id}", response_model=MujerOut)
def editar_mujer(mujer_id: int, actualizacion: MujerUpdate, db: Session = Depends(get_db)):
    mujer = db.query(Mujer).filter(Mujer.id == mujer_id).first()
    if not mujer:
        raise HTTPException(status_code=404, detail="Mujer no encontrada")

    # Guardamos la fecha anterior para comparar después
    fecha_examen_anterior = mujer.fecha_examen

    # Aplicamos los cambios
    for campo, valor in actualizacion.dict(exclude_unset=True).items():
        setattr(mujer, campo, valor)

    db.commit()
    db.refresh(mujer)

    # =====================================================
    # AQUÍ ESTÁ LA MAGIA: Borramos notificaciones viejas
    # =====================================================
    if 'fecha_examen' in actualizacion.dict(exclude_unset=True):
        # Si cambió la fecha del examen (es decir, se renovó)
        if fecha_examen_anterior != mujer.fecha_examen:
            # Calculamos cuál era la fecha de vencimiento anterior
            fecha_vencimiento_anterior = fecha_examen_anterior + relativedelta(months=6) if fecha_examen_anterior else None

            # Borramos TODAS las notificaciones enviadas para esta mujer
            # (o solo la del vencimiento anterior, pero borrar todas es más limpio)
            deleted = db.query(NotificacionExamenEnviada).filter(
                NotificacionExamenEnviada.mujer_id == mujer_id
            ).delete()

            db.commit()

            print(f"Notificaciones antiguas eliminadas ({deleted}) para {mujer.nombre} al renovar examen")

    return mujer
@router.get("/mujeres/dueno/{dueno_id}", response_model=List[MujerOut])
def obtener_mujeres_por_dueno(dueno_id: int, db: Session = Depends(get_db)):
    mujeres = db.query(Mujer).filter(Mujer.dueno_id == dueno_id).all()
    # Los datos se mapean a MujerOut, que tiene 'documento'
    return mujeres

@router.get("/buscar_usuario/{usuario_id}", response_model=dict)
def obtener_nombre_por_id(usuario_id: int, db: Session = Depends(get_db)):
    dueno = db.query(Dueno).filter(Dueno.id == usuario_id).first()
    if dueno:
        return {"nombre": dueno.nombre, "rol": "dueño"}
    admin = db.query(Administrador).filter(Administrador.id == usuario_id).first()
    if admin:
        return {"nombre": admin.nombre, "rol": "administrador"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.get("/administradores/bar/{bar_id}", response_model=List[AdministradorOut])
def obtener_administradores_por_bar(bar_id: int, db: Session = Depends(get_db)):
    admins = db.query(Administrador).filter(Administrador.bar_id == bar_id).all()
    return admins


@router.delete("/administradores/{admin_id}", response_model=dict)
def eliminar_administrador(admin_id: int, db: Session = Depends(get_db)):
    admin = db.query(Administrador).filter(Administrador.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Administrador no encontrado")

    db.delete(admin)
    db.commit()
    return {"mensaje": "Administrador eliminado correctamente"}
@router.put("/administradores/{admin_id}", response_model=AdministradorOut)
def actualizar_administrador(admin_id: int, datos: AdministradorUpdate, db: Session = Depends(get_db)):
    admin = db.query(Administrador).filter(Administrador.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Administrador no encontrado")
    
    # Actualizar nombre
    if datos.nombre is not None and datos.nombre != admin.nombre:
        if db.query(Dueno).filter(Dueno.nombre == datos.nombre).first():
            raise HTTPException(status_code=400, detail="Ese nombre ya pertenece a un dueño")
        admin.nombre = datos.nombre
    
    # Actualizar correo
    if datos.correo is not None and datos.correo != admin.correo:
        if db.query(Administrador).filter(Administrador.correo == datos.correo).filter(Administrador.id != admin_id).first():
            raise HTTPException(status_code=400, detail="Ese correo ya está registrado.")
        admin.correo = datos.correo
    
    # ✅ NUEVO: Actualizar documento
    if datos.documento is not None and datos.documento != admin.documento:
        if db.query(Administrador).filter(Administrador.documento == datos.documento).filter(Administrador.id != admin_id).first():
            raise HTTPException(status_code=400, detail="Ese documento ya está registrado.")
        admin.documento = datos.documento

    # Actualizar otros campos
    if datos.telefono is not None:
        admin.telefono = datos.telefono
        
    if datos.foto is not None:
        admin.foto = datos.foto

    if datos.contraseña is not None:
        hashed_password = pwd_context.hash(datos.contraseña)
        admin.contraseña = hashed_password

    db.commit()
    db.refresh(admin)
    return admin
@router.post("/tareas_crear", response_model=TareaOut)
def crear_tarea(tarea: TareaCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva tarea y envía notificación por correo al administrador asignado.
    """
    try:
        # Buscar el administrador para obtener su correo y nombre
        administrador = db.query(Administrador).filter(
            Administrador.id == tarea.administrador_id
        ).first()
        
        if not administrador:
            raise HTTPException(
                status_code=404, 
                detail=f"Administrador con ID {tarea.administrador_id} no encontrado"
            )
        
        # Verificar que el administrador tenga correo
        if not administrador.correo:
            raise HTTPException(
                status_code=400,
                detail=f"El administrador {administrador.nombre} no tiene un correo registrado"
            )
        
        # Obtener el nombre del bar y del dueño
        bar_nombre = None
        dueno_nombre = None
        
        if administrador.bar_id:
            bar = db.query(Bar).filter(Bar.id == administrador.bar_id).first()
            if bar:
                bar_nombre = bar.nombre
                # Obtener el nombre del dueño del bar
                if bar.dueno_id:
                    dueno = db.query(Dueno).filter(Dueno.id == bar.dueno_id).first()
                    if dueno:
                        dueno_nombre = dueno.nombre
        
        # Crear la tarea en la base de datos
        nueva_tarea = Tarea(**tarea.dict())
        db.add(nueva_tarea)
        db.commit()
        db.refresh(nueva_tarea)
        
        # Enviar el correo al administrador
        enviar_email_tarea(
            destinatario=administrador.correo,
            admin_nombre=administrador.nombre,
            descripcion=tarea.descripcion,
            fecha=tarea.fecha.strftime('%d/%m/%Y'),
            bar_nombre=bar_nombre,
            dueno_nombre=dueno_nombre
        )
        
        return nueva_tarea
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear la tarea: {str(e)}"
        )
@router.get("/tareas_ver/{administrador_id}", response_model=List[TareaOut])
def obtener_tareas_por_admin(administrador_id: int, db: Session = Depends(get_db)):
    tareas = db.query(Tarea).filter(Tarea.administrador_id == administrador_id).all()
    return tareas

@router.put("/tareas/{tarea_id}/completar", response_model=schemas.TareaOut)
def completar_tarea(
    tarea_id: int,
    db: Session = Depends(get_db)
):
    tarea = db.query(modelos.Tarea).filter(modelos.Tarea.id == tarea_id).first()
    if not tarea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La tarea con el id {tarea_id} no fue encontrada."
        )
    tarea.estado = "completada"
    tarea.fecha_completada = date.today()
    db.commit()
    db.refresh(tarea)
    return tarea

@router.delete("/tareas_eliminar/{tarea_id}", response_model=dict)
def eliminar_tarea(tarea_id: int, db: Session = Depends(get_db)):
    tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    db.delete(tarea)
    db.commit()
    return {"mensaje": "Tarea eliminada correctamente"}
@router.get("/productos_por_bar/{bar_id}", response_model=List[ProductoOut])
def obtener_productos_por_bar(
    bar_id: int,
    db: Session = Depends(get_db),
    # Nuevos parámetros para paginación (default: primera página de 20 elementos)
    skip: int = Query(0, ge=0, description="Número de productos a saltar (offset)"),
    limit: int = Query(20, gt=0, le=100, description="Número máximo de productos a devolver (límite por página)")
):
    """
    Obtiene una lista paginada de productos 'activos' de un bar específico.
    """
    productos = db.query(Producto).filter(
        Producto.bar_id == bar_id,
        Producto.estado == 'activo'
    ).offset(skip).limit(limit).all()

    return productos



@router.get("/tareas_pendientes_count/{admin_id}")
async def get_tareas_pendientes_count(admin_id: int, db: Session = Depends(get_db)):
    count = db.query(Tarea).filter(
        Tarea.administrador_id == admin_id,
        Tarea.estado == "pendiente"
    ).count()
    
    return {"pendientes": count}  # ← esto está perfecto
@router.post("/crear_productos", response_model=ProductoOut)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):

    nuevo_producto = Producto(**producto.dict())
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    mensaje_historial = f"Se agregó correctamente el producto: {nuevo_producto.nombre}."
    tipo_historial = "agrego"
    agregar_a_historial(
        db=db,
        bar_id=nuevo_producto.bar_id,
        producto_id=nuevo_producto.id,
        mensaje=mensaje_historial,
        tipo=tipo_historial
    )
    db.commit()
    
    return nuevo_producto

@router.delete("/eliminar_producto/{producto_id}")
def eliminar_producto_logico(producto_id: int, db: Session = Depends(get_db)):
    producto_a_eliminar = db.query(modelos.Producto).filter(modelos.Producto.id == producto_id).first()

    if not producto_a_eliminar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado.")

    # 1. Marcar el producto como "eliminado"
    producto_a_eliminar.estado = 'eliminado'
    db.commit()
    db.refresh(producto_a_eliminar)

    # 2. Registrar la acción en el historial
    mensaje_historial = f"Se eliminado el producto: {producto_a_eliminar.nombre}."
    tipo_historial = "elimino"
    agregar_a_historial(
        db=db,
        bar_id=producto_a_eliminar.bar_id,
        producto_id=producto_a_eliminar.id,
        mensaje=mensaje_historial,
        tipo=tipo_historial
    )
    db.commit() # ¡IMPORTANTE! Agregar este commit para guardar el historial
    
    return {"mensaje": f"Producto '{producto_a_eliminar.nombre}' ha sido marcado como eliminado."}


from fastapi import HTTPException, status
import logging

# Esto te va a mostrar TODO en la consola
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def agregar_a_historial(
    db: Session,
    bar_id: int,
    producto_id: int,
    mensaje: str,
    tipo: str
):
    logger.info("ENTRAMOS A agregar_a_historial !!!")
    logger.info(f"bar_id: {bar_id}, producto_id: {producto_id}")
    logger.info(f"mensaje: {mensaje}")
    logger.info(f"tipo: {tipo}")

    nuevo = Historial(
        bar_id=bar_id,
        producto_id=producto_id,
        mensaje=mensaje,
        tipo=tipo,
        tiempo=datetime.now()
    )
    db.add(nuevo)
    logger.info("Historial agregado a la sesión con db.add()")
    logger.info(f"ID del nuevo historial (aún sin commit): {nuevo.id}")  # Será None hasta el commit



@router.put("/editar_producto/{producto_id}", response_model=ProductoOut)
def editar_producto(producto_id: int, producto_data: ProductoUpdate, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    for campo, valor in producto_data.dict(exclude_unset=True).items():
        setattr(producto, campo, valor)

    db.commit()
    db.refresh(producto)
    return producto
@router.patch("/actualizar_productos/{producto_id}")
@router.put("/actualizar_productos/{producto_id}")  # Soporta ambos métodos
def actualizar_producto(
    producto_id: int,
    producto_update: schemas.ProductoUpdate,
    db: Session = Depends(get_db)
):
    producto_db = db.query(modelos.Producto).filter(modelos.Producto.id == producto_id).first()
    if not producto_db:
        raise HTTPException(status_code=404, detail=f"Producto con ID {producto_id} no encontrado.")

    update_data = producto_update.dict(exclude_unset=True)
    
    # === DETECCIÓN Y REGISTRO BONITO DEL CAMBIO DE STOCK ===
    if "cantidad" in update_data:
        nueva = update_data["cantidad"]
        anterior = producto_db.cantidad
        diferencia = nueva - anterior

        if diferencia > 0:
            mensaje = f"➕ Aumentó {producto_db.nombre}: +{diferencia} und"
            tipo = "aumento"
        elif diferencia < 0:
            mensaje = f"➖ Disminuyó {producto_db.nombre}: -{abs(diferencia)} und"
            tipo = "disminuyo"
        else:
            mensaje = f"✏️ Ajuste en {producto_db.nombre} (sin cambio)"
            tipo = "ajuste"

        # Guardamos el historial con el mensaje bonito
        agregar_a_historial(
            db=db,
            bar_id=producto_db.bar_id,
            producto_id=producto_db.id,
            mensaje=mensaje,
            tipo=tipo
        )

    # Aplicar todos los cambios recibidos (nombre, precio, imagen, cantidad, etc.)
    for key, value in update_data.items():
        setattr(producto_db, key, value)

    # Un solo commit: actualiza producto + guarda historial
    db.commit()
    db.refresh(producto_db)

    return producto_db

@router.get("/historial/bar/{bar_id}", response_model=List[HistorialSimpleOut])
def obtener_historial_por_bar(
    bar_id: int, 
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    historial_query = db.query(Historial).filter(Historial.bar_id == bar_id)

    historial_paginado = historial_query.order_by(desc(Historial.tiempo)).offset(skip).limit(limit).all()

    if not historial_paginado:
        return []

    return historial_paginado




@router.get("/productos_por_bar2/{bar_id}", response_model=List[schemas.ProductoOut])
def get_productos_para_facturar(bar_id: int, db: Session = Depends(get_db)):

    productos = db.query(modelos.Producto).filter(
        modelos.Producto.bar_id == bar_id,
        modelos.Producto.cantidad > 0,
        modelos.Producto.estado == 'activo'  # ← AQUÍ ESTÁ LA CLAVE
    ).all()
    
    if not productos:
        return []
    
    return productos
@router.post("/generar_factura", response_model=schemas.FacturaOut, status_code=status.HTTP_201_CREATED)
def generar_factura(factura_data: schemas.FacturaCreateRequest, db: Session = Depends(get_db)):    
    db_bar = db.query(modelos.Bar).filter(modelos.Bar.id == factura_data.bar_id).first()
    db_admin = db.query(modelos.Administrador).filter(modelos.Administrador.id == factura_data.administrador_id).first()
    if not db_bar or not db_admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bar o administrador no encontrado")
    total_ingresos = 0.0
    detalles_factura_modelos = []
    detalles_para_email = []
    for item in factura_data.productos:
        db_producto = db.query(modelos.Producto).filter(modelos.Producto.id == item.producto_id).first()
        if not db_producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Producto con ID {item.producto_id} no encontrado")
        
        if item.cantidad_final < 0 or item.cantidad_final > db_producto.cantidad:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cantidad final para el producto '{db_producto.nombre}' es inválida."
            )
        cantidad_vendida = db_producto.cantidad - item.cantidad_final
        subtotal = cantidad_vendida * db_producto.precio
        cantidad_inicial_producto = db_producto.cantidad
        db_producto.cantidad = item.cantidad_final
        db.add(db_producto)
        detalle = modelos.DetalleFactura(
            producto_id=db_producto.id,
            nombre_producto=db_producto.nombre,
            precio_unitario=db_producto.precio,
            cantidad_inicial=cantidad_inicial_producto,
            cantidad_final=item.cantidad_final,
            cantidad_vendida=cantidad_vendida,
            subtotal=subtotal
        )
        detalles_factura_modelos.append(detalle)
        total_ingresos += subtotal
        detalles_para_email.append(schemas.DetalleFacturaOut(
            id=0,
            producto_id=db_producto.id,
            nombre_producto=db_producto.nombre,
            imagen_producto=db_producto.imagen,
            cantidad_inicial=cantidad_inicial_producto,
            cantidad_final=item.cantidad_final,
            cantidad_vendida=cantidad_vendida,
            precio_unitario=db_producto.precio,
            subtotal=subtotal
        ))
    total_gastos = 0.0
    gastos_modelos = []
    gastos_para_email = []
    if factura_data.gastos_hormiga:
        for gasto_in in factura_data.gastos_hormiga:
            total_gastos += gasto_in.precio
            gasto_modelo = modelos.Gasto(
                nombre=gasto_in.nombre,
                precio=gasto_in.precio
            )
            gastos_modelos.append(gasto_modelo)
            
            gastos_para_email.append(schemas.GastoOut(
                id=0, nombre=gasto_in.nombre, precio=gasto_in.precio
            ))
    total_neto = total_ingresos - total_gastos
    nueva_factura = modelos.Factura(
        bar_id=factura_data.bar_id,
        administrador_id=factura_data.administrador_id,
        total_ingresos=total_ingresos,
        total_gastos=total_gastos,  
        total_neto=total_neto,  
        detalles_factura=detalles_factura_modelos,
        gastos=gastos_modelos,   
        fecha=datetime.now().date(),
        hora=datetime.now()
    )
    db.add(nueva_factura)
    db.commit()
    db.refresh(nueva_factura)
    db_dueno = db.query(modelos.Dueno).filter(modelos.Dueno.id == db_bar.dueno_id).first()
    if not db_dueno:
        print("Advertencia: Dueño del bar no encontrado. No se puede enviar el correo.")
        return nueva_factura
    fecha_formateada = nueva_factura.fecha.strftime("%d/%m/%Y")
    hora_formateada = nueva_factura.hora.strftime("%I:%M %p")
    invoice_data_for_email = schemas.FacturaData(
        id=nueva_factura.id,
        fecha=fecha_formateada,
        hora=hora_formateada,
        admin_nombre=db_admin.nombre,
        total_ingresos=nueva_factura.total_ingresos,
        total_gastos=nueva_factura.total_gastos, 
        total_neto=nueva_factura.total_neto, 
        detalles=detalles_para_email,
        gastos=gastos_para_email, 
        bar_nombre=db_bar.nombre
    )
    html_content = schemas.generate_invoice_html(invoice_data_for_email)
    asunto_correo = f"Factura del bar '{db_bar.nombre}' - {fecha_formateada} {hora_formateada}"
    try:
        send_email(db_dueno.correo, asunto_correo, html_content)
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
    return nueva_factura

@router.get("/facturas/{factura_id}/admin/{administrador_id}", response_model=schemas.FacturaOut)
def get_factura_by_admin(factura_id: int, administrador_id: int, db: Session = Depends(get_db)):
    """
    Obtiene una factura específica validando que pertenezca al administrador y bar correspondientes.
    """
    db_factura = db.query(modelos.Factura).filter(modelos.Factura.id == factura_id).first()
    if not db_factura:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada")
    if db_factura.administrador_id != administrador_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para ver esta factura")
    return db_factura
# app/routers/facturas.py

@router.get("/facturas/administrador/{administrador_id}/bar/{bar_id}", response_model=List[schemas.FacturaOut])
def get_facturas_by_admin_and_bar(
    administrador_id: int,
    bar_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10
):
    """
    Obtiene facturas paginadas generadas por un administrador para un bar.
    """
    facturas_query = db.query(modelos.Factura).options(
        joinedload(modelos.Factura.detalles_factura).joinedload(modelos.DetalleFactura.producto),
        joinedload(modelos.Factura.gastos)
    ).filter(
        modelos.Factura.administrador_id == administrador_id,
        modelos.Factura.bar_id == bar_id
    ).order_by(modelos.Factura.fecha.desc(), modelos.Factura.hora.desc())

    facturas = facturas_query.offset(skip).limit(limit).all()
    if not facturas:
        return []

    facturas_con_info = []
    for factura in facturas:
        detalles = []
        for detalle in factura.detalles_factura:
            detalle_dict = {
                "id": detalle.id,
                "producto_id": detalle.producto_id,
                "nombre_producto": detalle.nombre_producto,
                "precio_unitario": detalle.precio_unitario,
                "cantidad_inicial": detalle.cantidad_inicial,
                "cantidad_final": detalle.cantidad_final,
                "cantidad_vendida": detalle.cantidad_vendida,
                "subtotal": detalle.subtotal,
                "imagen_producto": detalle.producto.imagen if detalle.producto else None
            }
            detalles.append(detalle_dict)
        
        # ✅ Construir la lista de gastos detallados
        gastos = []
        for gasto in factura.gastos:
            gastos.append({
                "id": gasto.id,
                "nombre": gasto.nombre,
                "precio": gasto.precio
            })

        factura_dict = {
            "id": factura.id,
            "fecha": factura.fecha,
            "hora": factura.hora,
            "administrador_id": factura.administrador_id,
            "bar_id": factura.bar_id,
            "total_ingresos": factura.total_ingresos,
            "total_gastos": factura.total_gastos,
            "total_neto": factura.total_neto,
            "detalles_factura": detalles,
            "gastos": gastos,  # <-- ✨ Aquí se corrige
            "admin_nombre": factura.administrador_rel.nombre,
            "admin_foto": factura.administrador_rel.foto
        }
        facturas_con_info.append(factura_dict)

    return facturas_con_info
@router.post("/administradores", response_model=AdministradorOut)
def crear_administrador(admin: AdministradorCreate, db: Session = Depends(get_db)):
    # 1. Verificar si el nombre ya pertenece a un Dueño
    if db.query(Dueno).filter(Dueno.nombre == admin.nombre).first():
        raise HTTPException(status_code=400, detail="Ese nombre ya pertenece a un dueño")

    # 2. Verificar si el correo ya existe en la tabla de Administradores
    if db.query(Administrador).filter(Administrador.correo == admin.correo).first():
        raise HTTPException(status_code=400, detail="Ya existe un administrador con ese correo electrónico.")
    
    # ✅ 3. Verificar si el documento ya existe
    if db.query(Administrador).filter(Administrador.documento == admin.documento).first():
        raise HTTPException(status_code=400, detail="Ya existe un administrador con ese documento.")
    
    # 4. Determinar el nuevo ID
    max_id_dueno = db.query(func.max(Dueno.id)).scalar() or 0
    max_id_admin = db.query(func.max(Administrador.id)).scalar() or 0
    nuevo_id = max(max_id_dueno, max_id_admin) + 1

    # 5. Hashear la contraseña
    hashed_password = pwd_context.hash(admin.contraseña)

    # 6. Crear y guardar el nuevo administrador
    nuevo_admin = Administrador(
        id=nuevo_id,
        nombre=admin.nombre,
        correo=admin.correo,
        documento=admin.documento,  # ✅ AGREGAR ESTA LÍNEA
        foto=admin.foto,
        telefono=admin.telefono,
        contraseña=hashed_password,
        bar_id=admin.bar_id
    )

    db.add(nuevo_admin)
    db.commit()
    db.refresh(nuevo_admin)
    return nuevo_admin

@router.get("/bar_tipo/{bar_id}", response_model=BarOut)
async def obtener_bar(bar_id: int, db: Session = Depends(get_db)):
    """
    Obtiene la información completa de un bar por su ID
    """
    bar = db.query(Bar).filter(Bar.id == bar_id).first()
    if not bar:
        raise HTTPException(status_code=404, detail="Bar no encontrado")
    return bar
@router.get("/facturas/bar/{bar_id}", response_model=List[schemas.FacturaOut])
def get_facturas_by_bar(
    bar_id: int, 
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(15, ge=1, le=100)
):
    """
    Obtiene facturas de un bar con paginación para implementar scroll infinito.
    """
    facturas = db.query(modelos.Factura).options(
        joinedload(modelos.Factura.detalles_factura).joinedload(modelos.DetalleFactura.producto),
        joinedload(modelos.Factura.administrador_rel),
        joinedload(modelos.Factura.gastos) # ✅ Carga la relación de gastos
    ).filter(
        modelos.Factura.bar_id == bar_id
    ).order_by(modelos.Factura.fecha.desc(), modelos.Factura.hora.desc()).offset(skip).limit(limit).all()
    
    if not facturas:
        return []
    
    facturas_con_info = []
    for factura in facturas:
        detalles = []
        for detalle in factura.detalles_factura:
            detalle_dict = {
                "id": detalle.id,
                "producto_id": detalle.producto_id,
                "nombre_producto": detalle.nombre_producto,
                "precio_unitario": detalle.precio_unitario,
                "cantidad_inicial": detalle.cantidad_inicial,
                "cantidad_final": detalle.cantidad_final,
                "cantidad_vendida": detalle.cantidad_vendida,
                "subtotal": detalle.subtotal,
                "imagen_producto": detalle.producto.imagen if detalle.producto else None
            }
            detalles.append(detalle_dict)
        
        # ✅ Construir la lista de gastos
        gastos = [
            {"id": gasto.id, "nombre": gasto.nombre, "precio": gasto.precio}
            for gasto in factura.gastos
        ]

        # Construimos el objeto de respuesta con los datos cargados directamente
        factura_dict = {
            "id": factura.id,
            "fecha": factura.fecha,
            "hora": factura.hora,
            "administrador_id": factura.administrador_id,
            "bar_id": factura.bar_id,
            "total_ingresos": factura.total_ingresos,
            "total_gastos": factura.total_gastos,         # ✅ Agregar total de gastos
            "total_neto": factura.total_neto,             # ✅ Agregar total neto
            "detalles_factura": detalles,
            "gastos": gastos,                             # ✅ Agregar la lista de gastos
            "admin_nombre": factura.administrador_rel.nombre if factura.administrador_rel else "Desconocido",
            "admin_foto": factura.administrador_rel.foto if factura.administrador_rel else None
        }
        facturas_con_info.append(factura_dict)

    return facturas_con_info
@router.get("/verificar_dueno", response_model=Dict[str, bool])
def verificar_existencia_dueno(db: Session = Depends(get_db)):
    """
    Verifica si existe al menos un dueño en la base de datos.
    
    Retorna:
    - `{"existe_dueno": true}` si hay al menos un dueño.
    - `{"existe_dueno": false}` si no hay ningún dueño.
    """
    dueno = db.query(Dueno).first()
    
    if dueno:
        return {"existe_dueno": True}
    else:
        return {"existe_dueno": False}
    

@router.put("/dueno/{dueno_id}", response_model=schemas.DuenoOut)
def update_dueno_data(
    dueno_id: int, 
    dueno_update: schemas.DuenoUpdate, 
    db: Session = Depends(get_db)
):
    db_dueno = db.query(modelos.Dueno).filter(modelos.Dueno.id == dueno_id).first()
    if not db_dueno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dueño no encontrado"
        )

    db_dueno.nombre = dueno_update.nombre
    db_dueno.telefono = dueno_update.telefono
    db_dueno.correo = dueno_update.correo
    
    db.commit()
    db.refresh(db_dueno)
    return db_dueno
# Endpoint para actualizar la contraseña
@router.put("/dueno/{dueno_id}/password")
def update_dueno_password(
    dueno_id: int,
    password_data: schemas.PasswordUpdate,
    db: Session = Depends(get_db)
):
    db_dueno = db.query(modelos.Dueno).filter(modelos.Dueno.id == dueno_id).first()
    if not db_dueno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dueño no encontrado"
        )
    hashed_password = pwd_context.hash(password_data.new_password)
    db_dueno.contraseña = hashed_password

    db.commit()
    return {"message": "Contraseña actualizada exitosamente"}
@router.put("/dueno/{dueno_id}/photo")
def update_dueno_photo(
    dueno_id: int, 
    photo_data: schemas.PhotoUpdate, 
    db: Session = Depends(get_db)
):
    db_dueno = db.query(modelos.Dueno).filter(modelos.Dueno.id == dueno_id).first()
    if not db_dueno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dueño no encontrado"
        )
    
    db_dueno.imagen = photo_data.photo_url
    
    db.commit()
    db.refresh(db_dueno)
    return {"message": "Imagen de perfil actualizada exitosamente", "photoUrl": db_dueno.imagen}


def send_email(to_email: str, subject: str, html_content: str):
    """Envía un correo electrónico con contenido HTML."""
    try:
        email_user = os.getenv("EMAIL_USER")
        email_pass = os.getenv("EMAIL_PASS")
        email_host = os.getenv("EMAIL_HOST")
        email_port = int(os.getenv("EMAIL_PORT"))

        if not email_user or not email_pass:
            print("Error: Las credenciales de correo no están configuradas en las variables de entorno.")
            return

        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(html_content, 'html'))

        with smtplib.SMTP(email_host, email_port) as server:
            server.starttls()
            server.login(email_user, email_pass)
            server.sendmail(email_user, to_email, msg.as_string())
        
        print(f"Correo enviado exitosamente a {to_email}")
        
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

@router.post("/dueno/{dueno_id}/verify-password")
def verify_dueno_password(
    dueno_id: int,
    password_data: schemas.PasswordCheck,
    db: Session = Depends(get_db)
):
    """
    Verifica la contraseña actual del dueño.
    """
    db_dueno = db.query(modelos.Dueno).filter(modelos.Dueno.id == dueno_id).first()
    
    if not db_dueno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dueño no encontrado"
        )

    # Usa la función `verify` de `passlib` para comparar de forma segura
    if not pwd_context.verify(password_data.password, db_dueno.contraseña):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña incorrecta"
        )

    return {"message": "Contraseña verificada exitosamente"}
@router.post("/historial/bar/{bar_id}/eliminar-y-enviar-email", status_code=status.HTTP_200_OK)
async def delete_history_and_send_email_endpoint(bar_id: int, db: Session = Depends(get_db)):
    # 1. Obtener el historial del bar ANTES de borrarlo
    history_to_delete = db.query(modelos.Historial).filter(modelos.Historial.bar_id == bar_id).all()
    
    # 2. Obtener la información del dueño y el bar para el correo
    bar = db.query(modelos.Bar).filter(modelos.Bar.id == bar_id).first()
    if not bar:
        raise HTTPException(status_code=404, detail="Bar no encontrado")
        
    dueno = db.query(modelos.Dueno).filter(modelos.Dueno.id == bar.dueno_id).first()
    if not dueno:
        raise HTTPException(status_code=404, detail="Dueño del bar no encontrado")

    # 3. Preparar los datos para el correo (AQUÍ ES EL CAMBIO DE ORDEN)
    #    Se convierte el historial a un formato que Pydantic puede manejar
    #    sin necesidad de la sesión de la base de datos activa.
    history_data_for_email = schemas.HistorialEmailData(
        bar_nombre=bar.nombre,
        fecha_borrado=datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        historial=[schemas.HistorialEmailItem.from_orm(item) for item in history_to_delete]
    )
    
    # 4. Generar el HTML y enviar el correo (AHORA PUEDE EJECUTARSE)
    html_content = schemas.generate_history_html(history_data_for_email)
    send_email(to_email=dueno.correo, subject=f"Copia de seguridad del Historial de {bar.nombre}", html_content=html_content)

    # 5. Borrar el historial de la base de datos (AHORA ES EL ÚLTIMO PASO)
    db.query(modelos.Historial).filter(modelos.Historial.bar_id == bar_id).delete(synchronize_session=False)
    db.commit()

    return {"message": "Historial eliminado y copia enviada al correo del dueño."}
@router.post("/dueno/forgot-password")
def forgot_password(request: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)):
    """
    Busca al dueño por su correo, genera un token numérico y lo envía por email.
    """
    db_dueno = db.query(modelos.Dueno).filter(modelos.Dueno.correo == request.correo).first()

    if not db_dueno:
        return {"message": "Si el correo está registrado, recibirás un código para restablecer tu contraseña."}

    # Genera un código numérico seguro de 6 dígitos
    reset_code = f"{secrets.randbelow(1000000):06d}"
    expires_at = datetime.now() + timedelta(minutes=15)

    db.query(modelos.PasswordResetToken).filter(modelos.PasswordResetToken.dueno_id == db_dueno.id).delete()
    db.commit()

    new_token = modelos.PasswordResetToken(
        token=reset_code,
        dueno_id=db_dueno.id,
        expires_at=expires_at
    )
    db.add(new_token)
    db.commit()
    db.refresh(new_token)

    # Nuevo HTML para el correo, con un diseño más atractivo y tus colores
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Recuperación de Contraseña</title>
        <style>
            body {{
                font-family: sans-serif;
                background-color: #f4f4f4;
                color: #333;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                background-color: #ffffff;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                background-color: #000000;
                color: #ffffff;
                padding: 20px;
                text-align: center;
            }}
            .content {{
                padding: 30px;
                text-align: center;
                color: #000000;
            }}
            .code-box {{
                background-color: #ff69b4; /* Rosa */
                color: #ffffff;
                padding: 15px 30px;
                margin: 25px 0;
                font-size: 32px;
                font-weight: bold;
                border-radius: 8px;
                display: inline-block;
                letter-spacing: 5px;
            }}
            .footer {{
                background-color: #000000;
                color: #ffffff;
                padding: 20px;
                text-align: center;
                font-size: 12px;
            }}
            h2 {{
                color: #ff69b4; /* Rosa */
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Recuperación de Contraseña</h1>
            </div>
            <div class="content">
                <h2>Hola {db_dueno.nombre},</h2>
                <p>Hemos recibido una solicitud para restablecer tu contraseña. Usa el siguiente código numérico:</p>
                <div class="code-box">
                    {reset_code}
                </div>
                <p>Este código es válido por 15 minutos. Si no solicitaste este cambio, por favor ignora este correo.</p>
            
            </div>
            <div class="footer">
                <p> Control AS. Todos los derechos reservados.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        send_email(to_email=db_dueno.correo, subject="Recuperación de Contraseña", html_content=html_content)
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

    return {"message": "Si el correo está registrado, recibirás un código para restablecer tu contraseña."}
@router.post("/dueno/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """
    Verifica el token y actualiza la contraseña del dueño.
    """
    db_token = db.query(modelos.PasswordResetToken).filter(modelos.PasswordResetToken.token == request.token).first()

    if not db_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Código inválido.")

    if db_token.expires_at < datetime.now():
        db.delete(db_token)
        db.commit()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El código ha expirado.")

    db_dueno = db.query(modelos.Dueno).filter(modelos.Dueno.id == db_token.dueno_id).first()
    if not db_dueno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dueño no encontrado.")

    # Hashea la nueva contraseña antes de guardarla
    hashed_password = pwd_context.hash(request.nueva_contraseña)
    db_dueno.contraseña = hashed_password
    db.commit()

    # Elimina el token para que no se pueda volver a usar
    db.delete(db_token)
    db.commit()

    return {"message": "Contraseña actualizada exitosamente."}

@router.delete("/bares/{bar_id}/facturas")
def delete_all_bar_invoices(
    bar_id: int,
    db: Session = Depends(get_db)
):
    bar = db.query(Bar).filter(Bar.id == bar_id).first()
    if not bar:
        raise HTTPException(status_code=404, detail=f"Bar con ID {bar_id} no encontrado.")

    # 1. Borrar primero los hijos (detalles y gastos) - evita error de FK
    db.query(DetalleFactura).filter(
        DetalleFactura.factura_id.in_(
            db.query(Factura.id).filter(Factura.bar_id == bar_id)
        )
    ).delete(synchronize_session=False)

    db.query(Gasto).filter(
        Gasto.factura_id.in_(
            db.query(Factura.id).filter(Factura.bar_id == bar_id)
        )
    ).delete(synchronize_session=False)

    # 2. Ahora sí borrar las facturas
    db.query(Factura).filter(Factura.bar_id == bar_id).delete(synchronize_session=False)

    # 3. Borrar productos en estado eliminado (y su historial por cascade)
    db.query(Producto).filter(
        Producto.bar_id == bar_id,
        Producto.estado == "eliminado"
    ).delete(synchronize_session=False)

    # 4. Borrar registros de productos_eliminados
    db.query(ProductoEliminado).filter(ProductoEliminado.bar_id == bar_id).delete(synchronize_session=False)

    db.commit()

    return {
        "mensaje": "Limpieza completa realizada: facturas, detalles, gastos, productos eliminados y backup borrados."
    }

from dateutil.relativedelta import relativedelta  # ¡AGREGA ESTO ARRIBA SI NO LO TIENES!

from dateutil.relativedelta import relativedelta  # ← Asegúrate de tener esto al inicio del archivo

def chequear_y_notificar_examenes_vencidos():
    db = next(get_db())
    hoy = date.today()
    
    try:
        fecha_limite = hoy - relativedelta(months=6)

        mujeres_vencidas = db.query(Mujer).filter(
            Mujer.fecha_examen.is_not(None),
            Mujer.fecha_examen < fecha_limite
        ).all()

        for mujer in mujeres_vencidas:
            ya_notificado = db.query(NotificacionExamenEnviada).filter(
                NotificacionExamenEnviada.mujer_id == mujer.id,
                NotificacionExamenEnviada.fecha_vencimiento_notificada == mujer.fecha_examen
            ).first()

            if ya_notificado:
                continue

            dueno = db.query(Dueno).filter(Dueno.id == mujer.dueno_id).first()
            if not dueno or not dueno.correo:
                continue

            fecha_vencimiento = mujer.fecha_examen + relativedelta(months=6)
            dias_vencido = (hoy - fecha_vencimiento).days

            # Nuevo diseño ULTRA ALERTA
            subject = f"URGENTE: Examen médico VENCIDO - {mujer.nombre} ({dias_vencido} días)"
            
            html = f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="utf-8">
                <title>¡ALERTA! Examen Médico Vencido</title>
                <style>
                    body {{ margin: 0; padding: 0; background: #f4f4f4; font-family: 'Segoe UI', Arial, sans-serif; }}
                    .container {{ max-width: 650px; margin: 20px auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 15px 40px rgba(0,0,0,0.2); }}
                    .header {{ background: linear-gradient(135deg, #e74c3c, #c0392b); padding: 35px 20px; text-align: center; color: white; }}
                    .header h1 {{ margin: 0; font-size: 32px; font-weight: bold; }}
                    .alert-icon {{ font-size: 60px; margin-bottom: 10px; }}
                    .body {{ padding: 40px 30px; color: #333; line-height: 1.7; }}
                    .warning-box {{ background: #ffebee; border-left: 8px solid #e74c3c; padding: 20px; margin: 25px 0; border-radius: 8px; }}
                    .mujer-name {{ font-size: 28px; color: #e74c3c; font-weight: bold; margin: 20px 0; text-align: center; }}
                    .info-table {{ width: 100%; border-collapse: collapse; margin: 25px 0; }}
                    .info-table td {{ padding: 12px 15px; border-bottom: 1px solid #eee; }}
                    .label {{ font-weight: bold; color: #e74c3c; width: 40%; }}
                    .value {{ color: #222; }}
                    .urgent {{ color: #e74c3c; font-weight: bold; font-size: 18px; }}
                    .btn {{ display: block; width: 280px; margin: 30px auto; background: #e74c3c; color: white; text-align: center; padding: 18px; border-radius: 12px; text-decoration: none; font-weight: bold; font-size: 18px; box-shadow: 0 6px 15px rgba(231, 76, 60, 0.4); }}
                    .btn:hover {{ background: #c0392b; }}
                    .footer {{ background: #222; color: #aaa; padding: 25px; text-align: center; font-size: 13px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <div class="alert-icon">⚠️</div>
                        <h1>¡ALERTA!</h1>
                        <p style="margin:5px 0 0; font-size:18px;">Examen Médico VENCIDO</p>
                    </div>

                    <div class="body">
                        <p><strong>Hola {dueno.nombre}</strong>,</p>
                        
                        <div class="warning-box">
                            <p class="urgent">La siguiente trabajadora tiene su examen médico <strong>VENCIDO:</strong></p>
                        </div>

                        <h2 class="mujer-name">💃 {mujer.nombre.upper()}</h2>

                        <table class="info-table">
                            <tr>
                                <td class="label">Documento:</td>
                                <td class="value"><strong>{mujer.documento or 'No registrado'}</strong></td>
                            </tr>
                            <tr>
                                <td class="label">Teléfono:</td>
                                <td class="value"><strong>{mujer.telefono or 'No registrado'}</strong></td>
                            </tr>
                            <tr>
                                <td class="label">Último examen:</td>
                                <td class="value">{mujer.fecha_examen.strftime('%d/%m/%Y')}</td>
                            </tr>
                            <tr>
                                <td class="label">Venció el:</td>
                                <td class="value urgent">{fecha_vencimiento.strftime('%d/%m/%Y')}</td>
                            </tr>
                            <tr>
                                <td class="label">Días vencido:</td>
                                <td class="value urgent"><strong>{dias_vencido} día{'s' if dias_vencido != 1 else ''}</strong></td>
                            </tr>
                        </table>

                        <p style="text-align:center; font-size:18px; color:#e74c3c;">
                            Es importante renovar el examen médico cada 6 meses.
                        </p>
                    </div>

                    <div class="footer">
                        <p>Control AS © 2025 • Sistema de Gestión • Notificación Automática</p>
                    </div>
                </div>
            </body>
            </html>
            """

            send_email(dueno.correo, subject, html)

            db.add(NotificacionExamenEnviada(
                mujer_id=mujer.id,
                fecha_vencimiento_notificada=mujer.fecha_examen
            ))
            db.commit()

            print(f"[ALERTA] Correo CRÍTICO enviado → {mujer.nombre} | {dias_vencido} días vencida")

    except Exception as e:
        db.rollback()
        print(f"Error crítico en notificaciones: {e}")
    finally:
        db.close()


def limpiar_facturas_y_productos_eliminados_mensual():
    """
    Se ejecuta automáticamente el día 1 de cada mes a las 3:15 AM
    Borra facturas, detalles, gastos, productos eliminados y su backup
    para TODOS los bares → SIN enviar ningún correo
    """
    db: Session = next(get_db())
    try:
        bares = db.query(modelos.Bar).all()
        
        for bar in bares:
            # === LÓGICA DE BORRADO (exactamente igual que tu endpoint) ===
            # 1. Borrar detalles y gastos primero (por FK)
            db.query(modelos.DetalleFactura).filter(
                modelos.DetalleFactura.factura_id.in_(
                    db.query(modelos.Factura.id).filter(modelos.Factura.bar_id == bar.id)
                )
            ).delete(synchronize_session=False)

            db.query(modelos.Gasto).filter(
                modelos.Gasto.factura_id.in_(
                    db.query(modelos.Factura.id).filter(modelos.Factura.bar_id == bar.id)
                )
            ).delete(synchronize_session=False)

            # 2. Borrar facturas
            db.query(modelos.Factura).filter(modelos.Factura.bar_id == bar.id).delete(synchronize_session=False)

            # 3. Borrar productos en estado "eliminado"
            db.query(modelos.Producto).filter(
                modelos.Producto.bar_id == bar.id,
                modelos.Producto.estado == "eliminado"
            ).delete(synchronize_session=False)

            # 4. Borrar backup de productos eliminados
            db.query(modelos.ProductoEliminado).filter(modelos.ProductoEliminado.bar_id == bar.id).delete(synchronize_session=False)

            db.commit()

            print(f"[{datetime.now()}] Limpieza mensual automática completada → {bar.nombre} (ID: {bar.id})")

    except Exception as e:
        db.rollback()
        print(f"ERROR en limpieza mensual automática: {e}")
    finally:
        db.close()


# app/vistas.py → Reemplaza toda la función por esta
def limpiar_tareas_completadas_mensual():
    db: Session = next(get_db())
    try:
        # === 1. TOMAR TODAS LAS TAREAS COMPLETADAS (sin importar fecha) ===
        tareas_completadas = db.query(modelos.Tarea).options(
            joinedload(modelos.Tarea.administrador)
            .joinedload(modelos.Administrador.bar)
            .joinedload(modelos.Bar.dueno)
        ).filter(
            modelos.Tarea.estado == "completada"
        ).all()

        if not tareas_completadas:
            print(f"[{datetime.now()}] No hay tareas completadas. Nada que enviar ni borrar.")
            return

        print(f"[{datetime.now()}] ¡{len(tareas_completadas)} tareas completadas encontradas! Preparando correos...")

        # === 2. AGRUPAR POR BAR ===
        from collections import defaultdict
        tareas_por_bar = defaultdict(list)
        for tarea in tareas_completadas:
            if tarea.administrador and tarea.administrador.bar:
                tareas_por_bar[tarea.administrador.bar].append(tarea)

        # === 3. PROCESAR CADA BAR ===
        for bar, tareas_del_bar in tareas_por_bar.items():
            dueno = bar.dueno
            if not dueno or not dueno.correo:
                print(f"Bar {bar.nombre}: dueño sin correo → no se envía resumen")
                continue

            # Agrupar por administrador
            tareas_por_admin = defaultdict(list)
            for tarea in tareas_del_bar:
                tareas_por_admin[tarea.administrador].append(tarea)

            admins_data = []
            for admin, tareas_admin in tareas_por_admin.items():
                if not admin:
                    continue

                # Datos para el correo del admin
                data_admin = schemas.TareasEmailData(
                    bar_nombre=bar.nombre,
                    administrador_nombre=admin.nombre,
                    mes_anterior="Mes Anterior",  # Puedes poner lo que quieras aquí
                    tareas=[schemas.TareaCompletadaItem.from_orm(t) for t in tareas_admin]
                )
                admins_data.append(data_admin)

                # ENVIAR CORREO AL ADMINISTRADOR
                if admin.correo:
                    html = schemas.generate_tareas_admin_html(data_admin)
                    send_email(
                        to_email=admin.correo,
                        subject=f"✅ Tus tareas completadas - {bar.nombre}",
                        html_content=html
                    )
                    print(f"Correo enviado a → {admin.nombre} ({admin.correo})")

            # ENVIAR RESUMEN AL DUEÑO
            resumen = schemas.ResumenDuenoData(
                bar_nombre=bar.nombre,
                mes_anterior="Resumen Mensual",
                administradores=admins_data
            )
            html_dueno = schemas.generate_resumen_dueno_html(resumen)
            send_email(
                to_email=dueno.correo,
                subject=f"Resumen de tareas completadas - {bar.nombre}",
                html_content=html_dueno
            )
            print(f"Resumen enviado al dueño → {dueno.nombre} ({dueno.correo}) - {len(tareas_del_bar)} tareas")

        # === 4. AHORA SÍ: BORRAR TODAS LAS TAREAS COMPLETADAS ===
        borradas = db.query(modelos.Tarea).filter(modelos.Tarea.estado == "completada").delete()
        db.commit()
        print(f"[{datetime.now()}] ¡ÉXITO TOTAL! {borradas} tareas completadas eliminadas permanentemente.")

    except Exception as e:
        db.rollback()
        print(f"ERROR GRAVE: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

# =============== ENDPOINT CORREGIDO Y DEFINITIVO ===============
from fastapi import Request  # ← Agregar esta importación

@router.post("/inventario/guardar-con-factura")
async def guardar_inventario_con_factura(
    request: Request,  # ← AGREGAR REQUEST
    bar_id: int = Form(...),
    tipo_usuario: str = Form(...),
    usuario_id: int = Form(...),
    aumentos: Optional[str] = Form(None),
    nuevos: Optional[str] = Form(None),
    factura: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    import json
    import base64

    # === VALIDAR PERMISOS ===
    administrador_id = None
    dueno_id = None

    if tipo_usuario == "administrador":
        admin = db.query(Administrador).filter(
            Administrador.id == usuario_id,
            Administrador.bar_id == bar_id
        ).first()
        if not admin:
            raise HTTPException(status_code=403, detail="Administrador no autorizado")
        administrador_id = usuario_id
    else:
        bar_check = db.query(Bar).filter(Bar.id == bar_id, Bar.dueno_id == usuario_id).first()
        if not bar_check:
            raise HTTPException(status_code=403, detail="Dueño no autorizado")
        dueno_id = usuario_id

    # === LEER FACTURA ===
    archivo_binario = None
    nombre_archivo = None
    mime_type = None
    if factura and factura.filename:
        archivo_binario = await factura.read()
        nombre_archivo = factura.filename
        mime_type = factura.content_type

    # === DETERMINAR TIPO ===
    tipo_op = "aumento_stock"
    if nuevos and not aumentos:
        tipo_op = "nuevos_productos"
    elif nuevos and aumentos:
        tipo_op = "ambos"

    # === CREAR FACTURA INVENTARIO ===
    nueva_factura_inv = FacturaInventario(
        bar_id=bar_id,
        administrador_id=administrador_id,
        dueno_id=dueno_id,
        tipo_operacion=tipo_op,
        archivo_factura=archivo_binario,
        nombre_archivo=nombre_archivo,
        mime_type=mime_type
    )
    db.add(nueva_factura_inv)
    db.flush()

    # === PROCESAR AUMENTOS ===
    if aumentos:
        try:
            lista_aumentos = json.loads(aumentos)
            for item in lista_aumentos:
                prod = db.query(Producto).filter(
                    Producto.id == item['producto_id'],
                    Producto.bar_id == bar_id
                ).first()
                if not prod:
                    continue
                prod.cantidad += int(item['cantidad'])

                detalle = DetalleFacturaInventario(
                    factura_inventario_id=nueva_factura_inv.id,
                    producto_id=prod.id,
                    nombre_producto=prod.nombre,
                    cantidad=item['cantidad'],
                    es_nuevo_producto=False
                )
                db.add(detalle)
        except Exception as e:
            print(f"❌ Error procesando aumentos: {e}")
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error procesando aumentos: {str(e)}")

    # === ✅ PROCESAR PRODUCTOS NUEVOS CON IMÁGENES ===
    if nuevos:
        try:
            lista_nuevos = json.loads(nuevos)
            
            # ✅ Obtener TODOS los archivos del FormData
            form_data = await request.form()
            print(f"📦 Claves en FormData: {list(form_data.keys())}")
            
            for item in lista_nuevos:
                index = item.get('index', 0)
                imagen_base64 = None
                
                # ✅ Buscar la imagen correspondiente en el FormData
                imagen_key = f'imagen_{index}'
                print(f"🔍 Buscando clave: {imagen_key}")
                
                if imagen_key in form_data:
                    imagen_file = form_data[imagen_key]
                    print(f"📷 Imagen encontrada: {imagen_file.filename if hasattr(imagen_file, 'filename') else 'sin nombre'}")
                    
                    # ✅ Leer el archivo y convertirlo a base64
                    imagen_bytes = await imagen_file.read()
                    content_type = imagen_file.content_type if hasattr(imagen_file, 'content_type') else 'image/jpeg'
                    
                    # Convertir a base64 con prefijo data:image
                    imagen_base64 = f"data:{content_type};base64,{base64.b64encode(imagen_bytes).decode('utf-8')}"
                    print(f"✅ Imagen convertida a base64 ({len(imagen_base64)} caracteres)")
                else:
                    print(f"⚠️ No se encontró imagen para índice {index}")
                
                # ✅ Crear producto nuevo CON la imagen
                nuevo_prod = Producto(
                    nombre=item['nombre'],
                    precio=float(item['precio']),
                    cantidad=int(item['cantidad']),
                    imagen=imagen_base64,  # ✅ AHORA SÍ TIENE VALOR
                    bar_id=bar_id,
                    estado='activo'
                )
                db.add(nuevo_prod)
                db.flush()

                # ✅ Guardar detalle
                detalle = DetalleFacturaInventario(
                    factura_inventario_id=nueva_factura_inv.id,
                    producto_id=nuevo_prod.id,
                    nombre_producto=item['nombre'],
                    imagen_producto=imagen_base64,
                    cantidad=int(item['cantidad']),
                    precio_unitario=float(item['precio']),
                    es_nuevo_producto=True
                )
                db.add(detalle)
                
                print(f"✅ Producto creado: {nuevo_prod.nombre} (ID: {nuevo_prod.id}) - Imagen: {'Sí' if imagen_base64 else 'No'}")
                
        except json.JSONDecodeError as e:
            print(f"❌ Error decodificando JSON: {e}")
            db.rollback()
            raise HTTPException(status_code=400, detail="Formato JSON inválido")
        except Exception as e:
            print(f"❌ Error procesando productos nuevos: {e}")
            import traceback
            traceback.print_exc()
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    try:
        db.commit()
        print(f"✅ Inventario guardado (Factura ID: {nueva_factura_inv.id})")
    except Exception as e:
        db.rollback()
        print(f"❌ Error al commit: {e}")
        raise HTTPException(status_code=500, detail=f"Error guardando: {str(e)}")

    return {
        "mensaje": "Inventario actualizado con éxito",
        "factura_inventario_id": nueva_factura_inv.id
    }
def create_tables_and_seed_data():
    """Crea la tabla GestorPrincipal y añade el usuario por defecto."""
    
    # Base.metadata.create_all(bind=engine) # NO hace falta aquí, ya se llama en main.py

    with Session(engine) as session:
        gestor_existente = session.query(GestorPrincipal).filter(
            GestorPrincipal.correo == "barrantessebastian261@gmail.com"
        ).first()

        if gestor_existente is None:
            print("Creando usuario Gestor Principal por defecto...")
            
            hashed_password = get_password_hash("123456")
            
            gestor_principal = GestorPrincipal(
                nombre="diego Sebastián barrantes",
                correo="barrantessebastian261@gmail.com",
                contraseña=hashed_password
            )
            
            session.add(gestor_principal)
            session.commit()
            print("Gestor Principal creado exitosamente.")  

@router.post("/gestor_principal/login", response_model=GestorPrincipalLoginResponse, tags=["Gestores Principales"])
def login_gestor_principal(request: GestorPrincipalLoginRequest, db: Session = Depends(get_db)):
    """
    Inicia sesión para un Gestor Principal usando correo y contraseña.
    """
    # 1. Buscar al usuario por correo
    gestor = db.query(GestorPrincipal).filter(
        GestorPrincipal.correo == request.correo
    ).first()

    # 2. Verificar si el usuario existe
    if not gestor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario no encontrado o credenciales incorrectas"
        )

    # 3. Verificar la contraseña (debe estar hasheada en la DB)
    if not pwd_context.verify(request.contraseña, gestor.contraseña):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Contraseña incorrecta"
        )

    # 4. Login exitoso: Devolver SOLO los campos de la tabla
    return GestorPrincipalLoginResponse(
        id=gestor.id,
        nombre=gestor.nombre,
        correo=gestor.correo
    )


@router.get("/duenos", response_model=List[DuenoOut])
def obtener_duenos(db: Session = Depends(get_db)):
    return db.query(modelos.Dueno).all()
@router.put("/duenos/{dueno_id}", response_model=DuenoOut)
def actualizar_dueno(
    dueno_id: int,
    dueno_update: DuenoUpdate,
    db: Session = Depends(get_db)
):
    db_dueno = db.query(modelos.Dueno).filter(modelos.Dueno.id == dueno_id).first()
    if not db_dueno:
        raise HTTPException(status_code=404, detail="Dueño no encontrado")

    update_data = dueno_update.dict(exclude_unset=True)

    # Si intenta cambiar el nombre, validar que no exista otro con ese nombre
    if "nombre" in update_data:
        existe = db.query(modelos.Dueno).filter(
            modelos.Dueno.nombre == update_data["nombre"],
            modelos.Dueno.id != dueno_id
        ).first()
        if existe:
            raise HTTPException(status_code=400, detail="Ya existe otro dueño con ese nombre")

    # Si intenta cambiar el correo, validar que no exista
    if "correo" in update_data:
        existe = db.query(modelos.Dueno).filter(
            modelos.Dueno.correo == update_data["correo"],
            modelos.Dueno.id != dueno_id
        ).first()
        if existe:
            raise HTTPException(status_code=400, detail="El correo ya está en uso por otro dueño")

    # Aplicar los cambios (incluyendo cantidad_bares si viene en el update)
    for key, value in update_data.items():
        setattr(db_dueno, key, value)

    try:
        db.commit()
        db.refresh(db_dueno)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad: dato duplicado")

    return db_dueno

@router.delete("/duenos/{dueno_id}")
def eliminar_dueno(dueno_id: int, db: Session = Depends(get_db)):
    db_dueno = db.query(modelos.Dueno).filter(modelos.Dueno.id == dueno_id).first()
    if not db_dueno:
        raise HTTPException(status_code=404, detail="Dueño no encontrado")

    try:
        db.delete(db_dueno)
        db.commit()
        return {"detail": "Dueño eliminado correctamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al eliminar el dueño")
    

# === ENDPOINT 1: Listar facturas de inventario de un bar ===
@router.get("/inventario/facturas/{bar_id}")
async def obtener_facturas_inventario(
    bar_id: int,
    limit: int = 20, 
    last_id: int | None = None, 
    db: Session = Depends(get_db)
):
    """
    Obtiene facturas con scroll infinito (paginación por cursor),
    convirtiendo la hora de UTC a la hora local (America/Bogota, UTC-5)
    para la visualización.
    """
    
    # 💡 1. Definir la Zona Horaria Local (Colombia/Bogotá)
    ZONA_LOCAL = pytz.timezone('America/Bogota')
    
    query = db.query(FacturaInventario).filter(
        FacturaInventario.bar_id == bar_id
    )

    # 2. Paginación por cursor
    if last_id is not None:
        query = query.filter(FacturaInventario.id < last_id)

    facturas = query.order_by(
        FacturaInventario.fecha.desc(),
        FacturaInventario.hora.desc(),
        FacturaInventario.id.desc() 
    ).limit(limit).all()

    if not facturas:
        return []

    resultado = []
    for factura in facturas:
        
        # 💡 3. CONVERSIÓN DE HORA: UTC (DB) -> LOCAL (Visualización)
        
        # Asume que la hora guardada en la DB es UTC (naive o aware)
        hora_utc_naive = factura.hora
        
        # 3a. Hacer la hora 'aware' asumiendo que el valor guardado es UTC
        # Nota: Si el driver de SQLAlchemy ya devuelve objetos 'aware', 
        # esta línea puede variar, pero esto asegura la consistencia.
        hora_utc_aware = hora_utc_naive.replace(tzinfo=pytz.utc) 
        
        # 3b. Convertir de UTC a la zona horaria local (UTC-5)
        hora_local = hora_utc_aware.astimezone(ZONA_LOCAL)
        
        # 4. Obtener detalles y usuario
        detalles = db.query(DetalleFacturaInventario).filter(
            DetalleFacturaInventario.factura_inventario_id == factura.id
        ).all()
        
        total_aumentos = sum(1 for d in detalles if not d.es_nuevo_producto)
        total_nuevos = sum(1 for d in detalles if d.es_nuevo_producto)
        
        usuario_nombre = "Desconocido"
        if factura.administrador_id:
            admin = db.query(Administrador).get(factura.administrador_id)
            if admin: usuario_nombre = admin.nombre
        elif factura.dueno_id:
            dueno = db.query(Dueno).get(factura.dueno_id)
            if dueno: usuario_nombre = dueno.nombre

        resultado.append({
            "id": factura.id,
            "fecha": factura.fecha.isoformat(),
            # ✅ USAMOS LA HORA LOCAL CONVERTIDA
            "hora": hora_local.strftime("%I:%M %p"), # Ejemplo: 12:35 PM (Formato más legible)
            "hora_utc": factura.hora.isoformat(),   # Opcional: Para debugging, mantiene el UTC
            "tipo_operacion": factura.tipo_operacion,
            "tiene_factura": factura.archivo_factura is not None,
            "nombre_archivo": factura.nombre_archivo,
            "mime_type": factura.mime_type,
            "observaciones": factura.observaciones,
            "usuario_nombre": usuario_nombre,
            "total_aumentos": total_aumentos,
            "total_nuevos": total_nuevos
        })

    return resultado

# === ENDPOINT 2: Obtener detalles de una factura específica ===
@router.get("/inventario/factura/{factura_id}/detalles")
async def obtener_detalles_factura(
    factura_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene los detalles de productos de una factura de inventario
    → Si es un aumento y no tiene imagen guardada, la toma del producto actual
    """
    detalles = db.query(DetalleFacturaInventario).filter(
        DetalleFacturaInventario.factura_inventario_id == factura_id
    ).all()
    
    resultado = []
    for detalle in detalles:
        # ← AQUÍ ESTÁ EL FIX MÁGICO
        imagen_final = detalle.imagen_producto
        
        # Si es un aumento (no es nuevo) y no tiene imagen guardada → buscar en la tabla productos
        if not detalle.es_nuevo_producto and detalle.producto_id and (not imagen_final or imagen_final.strip() == ""):
            producto_actual = db.query(Producto).filter(
                Producto.id == detalle.producto_id
            ).first()
            if producto_actual and producto_actual.imagen:
                imagen_final = producto_actual.imagen

        resultado.append({
            "id": detalle.id,
            "producto_id": detalle.producto_id,
            "nombre_producto": detalle.nombre_producto,
            "imagen_producto": imagen_final,  # ← ahora SÍ siempre tiene imagen
            "cantidad": detalle.cantidad,
            "precio_unitario": detalle.precio_unitario,
            "es_nuevo_producto": detalle.es_nuevo_producto
        })
    
    return resultado

# === ENDPOINT 3: Descargar factura adjunta ===
@router.get("/inventario/factura/{factura_id}/descargar")
async def descargar_factura(
    factura_id: int,
    db: Session = Depends(get_db)
):
    """
    Descarga el archivo de factura adjunto
    """
    from fastapi.responses import Response
    
    factura = db.query(FacturaInventario).filter(
        FacturaInventario.id == factura_id
    ).first()
    
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    if not factura.archivo_factura:
        raise HTTPException(status_code=404, detail="Esta factura no tiene archivo adjunto")
    
    return Response(
        content=factura.archivo_factura,
        media_type=factura.mime_type or "application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename={factura.nombre_archivo or 'factura.pdf'}"
        }
    )

# === NUEVA FUNCIÓN (puedes ponerla en vistas.py o en main.py) ===
def backup_y_limpiar_facturas_inventario_mensual():
    from datetime import datetime, timezone
    from app.vistas import send_email

    db: Session = next(get_db())
    try:
        print("INICIANDO RESPALDO DEFINITIVO - CONTROL AS")

        def formato_tiempo_relativo(fecha, hora):
            """Convierte fecha/hora a formato simple"""
            if not fecha:
                return "Fecha no disponible"
            
            # Si hora es datetime, extraer solo el time; si es date, combinar
            if isinstance(hora, datetime):
                fecha_hora = hora
            elif isinstance(hora, type(hora)) and hasattr(hora, 'hour'):
                fecha_hora = datetime.combine(fecha, hora)
            else:
                fecha_hora = fecha if isinstance(fecha, datetime) else datetime.combine(fecha, datetime.min.time())
            
            # Formato de fecha simple en español
            meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
                    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
            return f"{fecha_hora.day} de {meses[fecha_hora.month-1]} de {fecha_hora.year}"

        bares = db.query(modelos.Bar).all()

        for bar in bares:
            if not bar.dueno or not bar.dueno.correo:
                continue

            facturas = db.query(modelos.FacturaInventario).filter(
                modelos.FacturaInventario.bar_id == bar.id
            ).order_by(modelos.FacturaInventario.fecha.desc(), modelos.FacturaInventario.hora.desc()).all()

            if not facturas:
                continue

            print(f"{bar.nombre} → {len(facturas)} movimientos encontrados")

            movimientos_html = ""
            total_movimientos = 0

            for factura in facturas:
                detalles = db.query(modelos.DetalleFacturaInventario).filter(
                    modelos.DetalleFacturaInventario.factura_inventario_id == factura.id
                ).all()

                total_movimientos += len(detalles)

                # Obtener nombre del usuario
                usuario = "Dueño del local"
                if factura.administrador_id:
                    admin = db.query(modelos.Administrador).get(factura.administrador_id)
                    usuario = admin.nombre if admin else "Administrador"
                elif factura.dueno_id:
                    usuario = bar.dueno.nombre

                # Formato de tiempo relativo
                tiempo = formato_tiempo_relativo(factura.fecha, factura.hora)

                # Crear filas de productos
                filas_productos = ""
                for det in detalles:
                    tipo = "Nuevo Producto" if det.es_nuevo_producto else "Aumento de Stock"
                    icono = "🆕" if det.es_nuevo_producto else "📈"
                    color_badge = "#ec4899" if det.es_nuevo_producto else "#3b82f6"
                    precio = f"${det.precio_unitario:,.0f}".replace(",", ".") if det.precio_unitario else "—"
                    
                    filas_productos += f"""
                    <tr style="border-bottom: 1px solid #f3f4f6;">
                        <td style="padding: 16px;">
                            <div style="display: inline-block; background: {color_badge}; color: white; padding: 5px 12px; border-radius: 16px; font-size: 0.8em; font-weight: 600;">
                                {icono} {tipo}
                            </div>
                        </td>
                        <td style="padding: 16px; font-size: 1em; font-weight: 600; color: #1f2937;">{det.nombre_producto}</td>
                        <td style="padding: 16px; text-align: center;">
                            <span style="background: #fce7f3; color: #ec4899; padding: 6px 14px; border-radius: 10px; font-weight: 700; font-size: 1em;">
                                {det.cantidad}
                            </span>
                        </td>
                        <td style="padding: 16px; text-align: right; font-size: 1em; font-weight: 700; color: #059669;">{precio}</td>
                    </tr>
                    """

                movimientos_html += f"""
                <div style="margin: 20px 0; background: white; border-radius: 16px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.08); border: 1px solid #f3f4f6;">
                    
                    <!-- Header con ID de factura -->
                    <div style="background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%); padding: 12px 20px; border-bottom: 2px solid #e5e7eb;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="color: #6b7280; font-size: 0.85em; font-weight: 600;">
                                📋 ID Factura: <span style="color: #1f2937; font-weight: 700;">#{factura.id}</span>
                            </span>
                            <span style="color: #6b7280; font-size: 0.85em; font-weight: 600;">
                                🏪 Bar ID: <span style="color: #1f2937; font-weight: 700;">#{bar.id}</span>
                            </span>
                        </div>
                    </div>
                    
                    <!-- Header con usuario y tiempo -->
                    <div style="background: linear-gradient(135deg, #1f2937 0%, #111827 100%); padding: 20px 24px;">
                        <div style="display: inline-block; background: rgba(236,72,152,0.2); border: 2px solid #ec4899; padding: 4px 12px; border-radius: 16px; margin-bottom: 8px;">
                            <span style="color: #ec4899; font-size: 0.75em; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">Registrado por</span>
                        </div>
                        <h3 style="margin: 0; font-size: 1.3em; color: white; font-weight: 700;">{usuario}</h3>
                        <p style="margin: 8px 0 0; color: #9ca3af; font-size: 0.9em; font-weight: 500;">
                            📅 {tiempo}
                        </p>
                    </div>

                    <!-- Tabla de productos -->
                    <div style="padding: 0;">
                        <table style="width: 100%; border-collapse: collapse;">
                            <thead>
                                <tr style="background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%); border-bottom: 2px solid #e5e7eb;">
                                    <th style="padding: 14px 16px; text-align: left; font-size: 0.85em; font-weight: 700; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px;">Tipo</th>
                                    <th style="padding: 14px 16px; text-align: left; font-size: 0.85em; font-weight: 700; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px;">Producto</th>
                                    <th style="padding: 14px 16px; text-align: center; font-size: 0.85em; font-weight: 700; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px;">Cantidad</th>
                                    <th style="padding: 14px 16px; text-align: right; font-size: 0.85em; font-weight: 700; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px;">Precio</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filas_productos}
                            </tbody>
                        </table>
                    </div>
                </div>
                """

            # EMAIL COMPLETO CON DISEÑO MODERNO
            html = f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>CONTROL AS - Respaldo de Inventario</title>
            </head>
            <body style="margin: 0; padding: 0; background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
                
                <div style="max-width: 800px; margin: 30px auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 15px 50px rgba(0,0,0,0.12);">
                    
                    <!-- Header Principal -->
                    <div style="background: linear-gradient(135deg, #111827 0%, #1f2937 100%); padding: 30px 24px; text-align: center;">
                        <div style="background: white; width: 60px; height: 60px; margin: 0 auto 16px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.8em; box-shadow: 0 6px 20px rgba(0,0,0,0.2);">
                            📊
                        </div>
                        <h1 style="margin: 0; font-size: 1.8em; color: white; font-weight: 800;">CONTROL AS</h1>
                        <p style="margin: 10px 0 0; font-size: 0.95em; color: #9ca3af; font-weight: 500;">Respaldo Mensual de Inventario</p>
                        
                        <!-- NOMBRE E ID DEL BAR AL PRINCIPIO -->
                        <div style="margin-top: 20px; background: rgba(255,255,255,0.1); padding: 16px 24px; border-radius: 12px; border: 2px solid rgba(236,72,152,0.3);">
                            <div style="color: #ec4899; font-size: 0.85em; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;">
                                🏪 Establecimiento
                            </div>
                            <div style="color: white; font-size: 1.5em; font-weight: 800; margin-bottom: 8px;">
                                {bar.nombre}
                            </div>
                            <div style="color: #9ca3af; font-size: 0.9em; font-weight: 600;">
                                ID del Bar: <span style="color: #ec4899; font-weight: 700;">#{bar.id}</span>
                            </div>
                        </div>
                    </div>

                    <!-- Contenido Principal -->
                    <div style="padding: 30px 24px;">
                        <h2 style="margin: 0 0 20px; font-size: 1.3em; color: #111827; font-weight: 700;">Movimientos de tus Administradores</h2>
                        
                        {movimientos_html}
                    </div>

                    <!-- Footer de Confirmación -->
                    <div style="background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%); padding: 30px; text-align: center; border-top: 2px solid #e5e7eb;">
                        <div style="display: inline-block; background: #10b981; color: white; padding: 10px 24px; border-radius: 25px; font-weight: 700; font-size: 1em; margin-bottom: 16px;">
                            ✓ Respaldo Completado
                        </div>
                        <p style="margin: 0; color: #6b7280; font-size: 0.95em; line-height: 1.6;">
                            Toda la información ha sido respaldada con éxito y eliminada de la base de datos.<br>
                            <strong>Tu sistema ahora está optimizado y funcionando al máximo rendimiento.</strong>
                        </p>
                    </div>

                    <!-- Footer Final -->
                    <div style="background: #111827; padding: 24px; text-align: center;">
                        <p style="margin: 0; color: #9ca3af; font-size: 0.9em;">
                            <strong style="color: white;">CONTROL AS</strong> • Sistema de Gestión Premium<br>
                            {datetime.now().strftime('%d de %B de %Y • %H:%M')}
                        </p>
                    </div>

                </div>

            </body>
            </html>
            """

            send_email(
                to_email=bar.dueno.correo,
                subject=f"📊 CONTROL AS - Respaldo Completo: {bar.nombre} (ID #{bar.id}) • {total_movimientos} movimientos",
                html_content=html
            )

            # BORRAR TODO
            for factura in facturas:
                db.query(modelos.DetalleFacturaInventario).filter(
                    modelos.DetalleFacturaInventario.factura_inventario_id == factura.id
                ).delete()
                db.delete(factura)
            db.commit()

            print(f"✅ ÉXITO TOTAL → {bar.nombre} (ID #{bar.id}) ({total_movimientos} movimientos respaldados)")

    except Exception as e:
        db.rollback()
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()



@router.post("/gestor_principal/forgot-password")
def gestor_forgot_password(request: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)):
    """
    Envía código de recuperación al correo del Gestor Principal
    """
    gestor = db.query(modelos.GestorPrincipal).filter(modelos.GestorPrincipal.correo == request.correo).first()
    if not gestor:
        return {"message": "Si el correo está registrado, recibirás un código para restablecer tu contraseña."}

    # Generar código de 6 dígitos
    import secrets
    from datetime import datetime, timedelta

    reset_code = f"{secrets.randbelow(1000000):06d}"
    expires_at = datetime.now() + timedelta(minutes=15)

    # Eliminar tokens anteriores del gestor (usamos dueno_id NULL para identificarlo)
    db.query(modelos.PasswordResetToken).filter(modelos.PasswordResetToken.dueno_id.is_(None)).delete()
    db.commit()

    # Guardar nuevo token (reutilizamos la tabla, pero con dueno_id NULL)
    new_token = modelos.PasswordResetToken(
        token=reset_code,
        dueno_id=None,  # Esto lo diferencia de los tokens de dueños
        expires_at=expires_at
    )
    db.add(new_token)
    db.commit()

    # Correo bonito
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: sans-serif; background: #f0f2f5; padding: 20px; }}
            .container {{ max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center; }}
            .header {{ background: #667eea; color: white; padding: 20px; border-radius: 10px 10px 0 0; margin: -30px -30px 30px -30px; }}
            .code {{ font-size: 36px; font-weight: bold; color: #667eea; letter-spacing: 8px; margin: 30px 0; background: #f0f0ff; padding: 15px; border-radius: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Control AS - Panel Administrador</h1>
            </div>
            <h2>¡Hola {gestor.nombre}!</h2>
            <p>Solicitaste recuperar tu contraseña.</p>
            <p>Tu código de verificación es:</p>
            <div class="code">{reset_code}</div>
            <p>Este código expira en 15 minutos.</p>
            <p>Si no solicitaste esto, ignora este mensaje.</p>
        </div>
    </body>
    </html>
    """

    try:
        send_email(
            to_email=gestor.correo,
            subject="🔑 Recuperación de contraseña - Control AS",
            html_content=html_content
        )
    except Exception as e:
        print(f"Error enviando correo: {e}")

    return {"message": "Si el correo está registrado, recibirás un código para restablecer tu contraseña."}


@router.post("/gestor_principal/reset-password")
def gestor_reset_password(request: schemas.ResetPasswordRequest, db: Session = Depends(get_db)):
    """
    Cambia la contraseña del Gestor Principal
    """
    from datetime import datetime

    db_token = db.query(modelos.PasswordResetToken).filter(
        modelos.PasswordResetToken.token == request.token,
        modelos.PasswordResetToken.dueno_id.is_(None)
    ).first()

    if not db_token:
        raise HTTPException(status_code=400, detail="Código inválido o ya utilizado.")

    if db_token.expires_at < datetime.now():
        db.delete(db_token)
        db.commit()
        raise HTTPException(status_code=400, detail="El código ha expirado.")

    # Como solo hay un Gestor Principal, lo buscamos directamente
    gestor = db.query(modelos.GestorPrincipal).first()
    if not gestor:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    # Cambiar contraseña
    hashed_password = pwd_context.hash(request.nueva_contraseña)
    gestor.contraseña = hashed_password
    db.commit()

    # Eliminar token usado
    db.delete(db_token)
    db.commit()

    return {"message": "¡Contraseña actualizada exitosamente!"}


# Después del endpoint forgot-password
@router.post("/gestor_principal/verify-reset-code")
def gestor_verify_reset_code(request: schemas.VerifyCodeRequest, db: Session = Depends(get_db)):
    """
    Verifica si el código de recuperación es válido (sin cambiar contraseña)
    """
    from datetime import datetime

    db_token = db.query(modelos.PasswordResetToken).filter(
        modelos.PasswordResetToken.token == request.token,
        modelos.PasswordResetToken.dueno_id.is_(None)
    ).first()

    if not db_token:
        raise HTTPException(status_code=400, detail="Código inválido o ya utilizado.")

    if db_token.expires_at < datetime.now():
        db.delete(db_token)
        db.commit()
        raise HTTPException(status_code=400, detail="El código ha expirado.")

    return {"message": "Código válido", "token": request.token}





@router.get("/gestor_principal", response_model=GestorPrincipalOut)
def obtener_gestor_principal(db: Session = Depends(get_db)):
    """Obtiene los datos del único Gestor Principal"""
    gestor = db.query(GestorPrincipal).first()
    if not gestor:
        raise HTTPException(status_code=404, detail="Gestor Principal no encontrado")
    return gestor


@router.put("/gestor_principal/update", response_model=GestorPrincipalOut)
def actualizar_gestor_principal(
    update_data: GestorPrincipalUpdate,
    current_password: str = Form(...),  # Se enviará desde frontend
    db: Session = Depends(get_db)
):
    """Actualiza nombre y/o correo del Gestor Principal (requiere contraseña actual)"""
    gestor = db.query(GestorPrincipal).first()
    if not gestor:
        raise HTTPException(status_code=404, detail="Gestor Principal no encontrado")

    # Verificar contraseña actual
    if not pwd_context.verify(current_password, gestor.contraseña):
        raise HTTPException(status_code=401, detail="Contraseña actual incorrecta")

    # Validar correo único si se está cambiando
    if update_data.correo and update_data.correo != gestor.correo:
        if db.query(GestorPrincipal).filter(GestorPrincipal.correo == update_data.correo).first():
            raise HTTPException(status_code=400, detail="El correo ya está en uso")

    # Aplicar cambios
    if update_data.nombre:
        gestor.nombre = update_data.nombre
    if update_data.correo:
        gestor.correo = update_data.correo

    db.commit()
    db.refresh(gestor)
    return gestor


@router.put("/gestor_principal/password")
def cambiar_contraseña_gestor(
    password_data: GestorPrincipalPasswordUpdate,
    db: Session = Depends(get_db)
):
    """Cambia la contraseña del Gestor Principal"""
    gestor = db.query(GestorPrincipal).first()
    if not gestor:
        raise HTTPException(status_code=404, detail="Gestor Principal no encontrado")

    # Verificar contraseña actual
    if not pwd_context.verify(password_data.current_password, gestor.contraseña):
        raise HTTPException(status_code=401, detail="Contraseña actual incorrecta")

    # Validar que la nueva contraseña tenga al menos 6 caracteres
    if len(password_data.new_password) < 6:
        raise HTTPException(status_code=400, detail="La nueva contraseña debe tener al menos 6 caracteres")

    # Actualizar contraseña
    gestor.contraseña = pwd_context.hash(password_data.new_password)
    db.commit()

    return {"message": "Contraseña actualizada exitosamente"}


@router.get("/hello")
def hello_test():
    return {"message": "¡Hola! La API está funcionando correctamente 🚀"}