# models.py - Modelos Corregidos y Completos con Cascade
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, ForeignKey, Date, Text, UniqueConstraint, func
from sqlalchemy.orm import relationship
from datetime import date, datetime, timezone
from conexion import Base
from sqlalchemy.dialects.mysql import DATETIME, LONGTEXT, LONGBLOB

from sqlalchemy.dialects.mysql import LONGTEXT, LONGBLOB
class GestorPrincipal(Base):
    __tablename__ = "gestores_principales"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    contraseña = Column(String(100), nullable=False)
# PERFIL GENERAL (Dueño del bar)
class Dueno(Base):
    __tablename__ = "duenos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    contraseña = Column(String(100), nullable=False)
    imagen = Column(LONGTEXT, nullable=True) 
    estado = Column(String(50), nullable=True)
    telefono = Column(String(50), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    cantidad_bares = Column(Integer, default=0, nullable=False)

    # Relación: un dueño puede tener varios bares y varias mujeres
    bares = relationship("Bar", back_populates="dueno", cascade="all, delete-orphan", passive_deletes=True)
    mujeres = relationship("Mujer", back_populates="dueno")
    

# BAR (local)
class Bar(Base):
    __tablename__ = "bares"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    ubicacion = Column(String(255), nullable=False)
    imagen = Column(LONGTEXT, nullable=True) 
    dueno_id = Column(Integer, ForeignKey("duenos.id", ondelete="CASCADE"), nullable=False)
    tipo = Column(String(50), default="bar", nullable=False)
    dueno = relationship("Dueno", back_populates="bares")
    
    # ✅ RELACIONES CON CASCADE - Eliminación en cascada
    administradores = relationship("Administrador", back_populates="bar", cascade="all, delete-orphan")
    productos = relationship("Producto", back_populates="bar", cascade="all, delete-orphan")
    historial_bares = relationship("Historial", back_populates="bar_rel", cascade="all, delete-orphan")
    productos_eliminados = relationship("ProductoEliminado", back_populates="bar", cascade="all, delete-orphan")
    facturas = relationship("Factura", back_populates="bar_rel", cascade="all, delete-orphan")


# MUJER
# MUJER (versión definitiva y súper limpia)
class Mujer(Base):
    __tablename__ = "mujeres"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    fecha_agregado = Column(DateTime, default=datetime.utcnow)
    documento = Column(String(255), nullable=True) 
    telefono = Column(String(50), nullable=True)
    foto = Column(LONGTEXT, nullable=True)
    agregado_por = Column(Integer, nullable=True)
    
    # ← SOLO ESTOS DOS CAMPOS (100% OPCIONALES)
    fecha_examen = Column(Date, nullable=True)          # Fecha del último examen médico
    foto_examen = Column(LONGTEXT, nullable=True)       # Foto o PDF del resultado (base64)

    dueno_id = Column(Integer, ForeignKey("duenos.id"))
    dueno = relationship("Dueno", back_populates="mujeres")

# ADMINISTRADOR
class Administrador(Base):
    __tablename__ = "administradores"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(255), unique=True, nullable=False)
    documento = Column(String(20), unique=True, nullable=False)
    foto = Column(LONGTEXT, nullable=True)
    fecha_agregado = Column(Date, default=date.today)
    telefono = Column(String(50), nullable=False)
    contraseña = Column(String(100), nullable=False)
    bar_id = Column(Integer, ForeignKey("bares.id"))
    
    bar = relationship("Bar", back_populates="administradores")
    
    # ✅ RELACIONES CON CASCADE - Eliminación en cascada
    tareas = relationship("Tarea", back_populates="administrador", cascade="all, delete-orphan")
    facturas = relationship("Factura", back_populates="administrador_rel", cascade="all, delete-orphan")


# TAREA
class Tarea(Base):
    __tablename__ = "tareas"
    id = Column(Integer, primary_key=True, index=True)
    administrador_id = Column(Integer, ForeignKey("administradores.id"))
    descripcion = Column(Text, nullable=False)
    fecha = Column(Date, nullable=False)
    estado = Column(String(50), nullable=False)
    fecha_completada = Column(Date, nullable=True)

    administrador = relationship("Administrador", back_populates="tareas")


# PRODUCTO
class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    imagen = Column(LONGTEXT, nullable=True)
    cantidad = Column(Integer, nullable=False)
    precio = Column(Float, nullable=False)
    bar_id = Column(Integer, ForeignKey("bares.id"))
    estado = Column(String(50), default='activo') 
    
    bar = relationship("Bar", back_populates="productos")
    
    # ✅ RELACIÓN CON CASCADE
    historial_productos = relationship("Historial", back_populates="producto_rel", cascade="all, delete-orphan")


# HISTORIAL
class Historial(Base):
    __tablename__ = "historial"
    id = Column(Integer, primary_key=True, index=True)
    bar_id = Column(Integer, ForeignKey("bares.id"))
    producto_id = Column(Integer, ForeignKey("productos.id", ondelete='SET NULL'), nullable=True) 
    
    mensaje = Column(String(255), nullable=False)
    tipo = Column(String(50), nullable=False)
    tiempo = Column(DateTime, server_default=func.now())

    bar_rel = relationship("Bar", back_populates="historial_bares")
    producto_rel = relationship("Producto", back_populates="historial_productos")


# PRODUCTO ELIMINADO
class ProductoEliminado(Base):
    __tablename__ = "productos_eliminados"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    imagen = Column(LONGTEXT, nullable=True)
    cantidad = Column(Integer, nullable=False)
    precio = Column(Float, nullable=False)
    bar_id = Column(Integer, ForeignKey("bares.id"))
    tiempo_eliminacion = Column(DateTime, server_default=func.now())

    bar = relationship("Bar", back_populates="productos_eliminados")


# FACTURA GENERAL
class Factura(Base):
    __tablename__ = "facturas"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, default=date.today)
    hora = Column(DateTime, default=datetime.utcnow)
    bar_id = Column(Integer, ForeignKey("bares.id"))
    administrador_id = Column(Integer, ForeignKey("administradores.id"))
    total_ingresos = Column(Float, nullable=False, default=0.0)
    total_gastos = Column(Float, nullable=False, default=0.0)
    total_neto = Column(Float, nullable=False, default=0.0)

    # ✅ RELACIONES CON CASCADE - Eliminación en cascada
    detalles_factura = relationship("DetalleFactura", back_populates="factura", cascade="all, delete-orphan")
    gastos = relationship("Gasto", back_populates="factura", cascade="all, delete-orphan")

    # Relación para obtener el bar y el administrador de la factura
    bar_rel = relationship("Bar", back_populates="facturas")
    administrador_rel = relationship("Administrador", back_populates="facturas")


# DETALLE DE CADA PRODUCTO EN LA FACTURA
class DetalleFactura(Base):
    __tablename__ = "detalles_factura"
    id = Column(Integer, primary_key=True, index=True)
    factura_id = Column(Integer, ForeignKey("facturas.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    nombre_producto = Column(String(100), nullable=False)
    precio_unitario = Column(Float, nullable=False)
    cantidad_inicial = Column(Integer, nullable=False)
    cantidad_final = Column(Integer, nullable=False)
    cantidad_vendida = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)

    # Relación con la factura a la que pertenece
    factura = relationship("Factura", back_populates="detalles_factura")
    producto = relationship("Producto")


# GASTO
class Gasto(Base):
    __tablename__ = "gastos"
    id = Column(Integer, primary_key=True, index=True)
    factura_id = Column(Integer, ForeignKey("facturas.id"), nullable=False)
    nombre = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)
    
    # Relación para asociar el gasto
    factura = relationship("Factura", back_populates="gastos")


# PASSWORD RESET TOKEN
class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), unique=True, nullable=False, index=True)
    dueno_id = Column(Integer, ForeignKey("duenos.id"))
    expires_at = Column(DateTime, nullable=False)


# models.py → al final del archivo
class NotificacionExamenEnviada(Base):
    __tablename__ = "notificaciones_examen_enviadas"
    
    id = Column(Integer, primary_key=True, index=True)
    mujer_id = Column(Integer, ForeignKey("mujeres.id", ondelete="CASCADE"), nullable=False)
    fecha_envio = Column(DateTime, server_default=func.now())
    fecha_vencimiento_notificada = Column(Date, nullable=False)
    
    # Esto hace que sea único por mujer + fecha de vencimiento
    __table_args__ = (UniqueConstraint('mujer_id', 'fecha_vencimiento_notificada', name='uniq_mujer_vencimiento'),)

# === NUEVAS TABLAS PARA GESTIÓN DE INVENTARIO CON FACTURA ===
class FacturaInventario(Base):
    __tablename__ = "facturas_inventario"
    
    id = Column(Integer, primary_key=True, index=True)
    bar_id = Column(Integer, ForeignKey("bares.id"), nullable=False)
    administrador_id = Column(Integer, ForeignKey("administradores.id"), nullable=True)
    dueno_id = Column(Integer, ForeignKey("duenos.id"), nullable=True)
    fecha = Column(Date, default=date.today, nullable=False)
    
    # AMBAS EN UTC, usando func.utc_timestamp() → garantizado UTC en MySQL
  
    hora = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    creado_el = Column(DateTime, server_default=func.now(), nullable=False) # Deja func.now() si no te da problemas
    
    tipo_operacion = Column(String(20), nullable=False)
    archivo_factura = Column(LONGBLOB, nullable=True)
    nombre_archivo = Column(String(255), nullable=True)
    mime_type = Column(String(100), nullable=True)
    observaciones = Column(Text, nullable=True)

    bar_rel = relationship("Bar")
    administrador_rel = relationship("Administrador")
    dueno_rel = relationship("Dueno")
    
    detalles = relationship("DetalleFacturaInventario", back_populates="factura_inventario", 
                            cascade="all, delete-orphan")
class DetalleFacturaInventario(Base):
    __tablename__ = "detalles_factura_inventario"
    
    id = Column(Integer, primary_key=True, index=True)
    factura_inventario_id = Column(Integer, ForeignKey("facturas_inventario.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=True)
    nombre_producto = Column(String(150), nullable=False)
    imagen_producto = Column(LONGTEXT, nullable=True) 
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=True)
    es_nuevo_producto = Column(Boolean, default=False)

    factura_inventario = relationship("FacturaInventario", back_populates="detalles")
    producto = relationship("Producto")