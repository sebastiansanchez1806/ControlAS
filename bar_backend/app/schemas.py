import calendar
from multiprocessing import get_context
from pydantic import BaseModel, Field, validator
from typing import Any, Optional, List
from datetime import date, datetime, timedelta
from passlib.context import CryptContext
from typing import Any
from requests import Session

from app import modelos
from conexion import get_db
class PasswordCheck(BaseModel):
    password: str
# --- Esquemas de Dueno ---
class DuenoBase(BaseModel):
    nombre: str
    correo: str
    contraseña: str
    imagen: Optional[str] = None
    estado: Optional[str] = None
    telefono: str
    cantidad_bares: int = 0  # ← 
class DuenoUpdate(BaseModel):
    nombre: str
    telefono: str
    correo: str

class PhotoUpdate(BaseModel):
    photo_url: str
    
class DuenoCreate(DuenoBase):
    pass

class DuenoOut(BaseModel):
    id: int
    nombre: str
    correo: str
    telefono: str
    cantidad_bares: int
    imagen: Optional[str] = None
    estado: Optional[str] = None
    
    class Config:
        from_attributes = True
class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str

# Nuevo esquema para la actualización de foto
class PhotoUpdate(BaseModel):
    photo_url: str
# --- Esquemas de Bar ---
class BarBase(BaseModel):
    nombre: str
    ubicacion: str
    imagen: Optional[str] = None
    dueno_id: int
    tipo: str = Field(default="bar")
    
    @validator('tipo')
    def validar_tipo_bar(cls, v):
        # 🔍 DEBUG: Ver qué valor llega
        print(f"🔍 Validando tipo recibido: '{v}' (tipo: {type(v).__name__})")
        
        tipos_permitidos = ["bar", "burdel"]
        
        # Convertir a minúsculas para comparar
        v_lower = str(v).lower().strip()
        print(f"🔍 Tipo normalizado: '{v_lower}'")
        
        if v_lower not in tipos_permitidos:
            print(f"❌ Tipo '{v_lower}' no está en {tipos_permitidos}")
            raise ValueError(f"El tipo de bar debe ser uno de: {', '.join(tipos_permitidos)}")
        
        print(f"✅ Tipo '{v_lower}' validado correctamente")
        return v_lower

    class Config:
        str_strip_whitespace = True  # Elimina espacios en blanco automáticamente
class BarCreate(BarBase):
    pass

class BarOut(BarBase):
    id: int
    class Config:
        from_attributes = True

class BarUpdate(BaseModel):
    nombre: Optional[str]
    ubicacion: Optional[str]
    imagen: Optional[str]

# --- Esquemas de Mujer ---
class MujerBase(BaseModel):
    nombre: str
    documento: Optional[str] = None
    telefono: Optional[str] = None
    foto: Optional[str] = None
    agregado_por: Optional[int] = None
    dueno_id: int
    
    # Para crear una mujer SÍ pueden ser obligatorios o no según tú quieras
    # (tú los quieres obligatorios al crear? déjalos así, si no → Optional también)
    fecha_examen: Optional[date] = None
    foto_examen: Optional[str] = None

class MujerCreate(MujerBase):
    # Si quieres que al crear sean obligatorios, haz esto:
    fecha_examen: date
    foto_examen: str
    # (Pydantic permite sobreescribir el tipo en la subclase)
class MujerOut(BaseModel):
    id: int
    nombre: str
    documento: Optional[str] = None
    telefono: Optional[str] = None
    foto: Optional[str] = None
    agregado_por: Optional[int] = None
    dueno_id: int
    fecha_agregado: datetime
    
    # ¡AHORA SÍ SON OPCIONALES EN LA RESPUESTA!
    fecha_examen: Optional[date] = None
    foto_examen: Optional[str] = None

    class Config:
        from_attributes = True
# Clase de actualización con la columna renombrada
class MujerUpdate(BaseModel):
    nombre: Optional[str] = None
    documento: Optional[str] = None
    telefono: Optional[str] = None
    foto: Optional[str] = None
    agregado_por: Optional[int] = None
    fecha_examen: Optional[date] = None
    foto_examen: Optional[str] = None
# --- Esquemas de Autenticación y Perfil ---
class LoginRequest(BaseModel):
    nombre: str
    contraseña: str
    bar_id: Optional[int] = None  

class LoginResponse(BaseModel):
    id: int
    nombre: str
    tipo: str
    telefono: str
    correo: Optional[str] = None
    imagen: Optional[str] = None
    foto: Optional[str] = None
    bar_id: Optional[int] = None
    dueno_id: Optional[int] = None
    bar_nombre: Optional[str] = None

# --- Esquemas de Administrador ---
class AdministradorBase(BaseModel):
    nombre: str
    correo: Optional[str] = None
    documento: Optional[str] = None  # ✅ NUEVO CAMPO
    foto: Optional[str] = None
    fecha_agregado: Optional[date] = None
    telefono: str
    contraseña: str
    bar_id: Optional[int] = None

class AdministradorOut(AdministradorBase):
    id: int
    class Config:
        from_attributes = True

class AdministradorCreate(BaseModel):
    nombre: str
    correo: str
    documento: str  # ✅ NUEVO CAMPO (requerido al crear)
    foto: Optional[str] = None
    fecha_agregado: Optional[date] = None
    telefono: str
    contraseña: str
    bar_id: int

class AdministradorUpdate(BaseModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    contraseña: Optional[str] = None
    foto: Optional[str] = None
    correo: Optional[str] = None
    documento: Optional[str] = None  # ✅ NUEVO CAMPO (opcional al actualizar)


# --- Esquemas de Tarea ---
class TareaBase(BaseModel):
    administrador_id: int
    descripcion: str
    fecha: date
    estado: str
    fecha_completada: Optional[date] = None

class TareaCreate(TareaBase):
    pass

class TareaOut(TareaBase):
    id: int
    class Config:
        from_attributes = True

class TareaUpdate(BaseModel):
    estado: str
    fecha_completada: Optional[date] = None

# --- Esquemas de Producto ---
class ProductoBase(BaseModel):
    nombre: str
    imagen: Optional[str] = None
    cantidad: int
    precio: float
    bar_id: int

class ProductoCreate(ProductoBase):
    pass

class ProductoOut(ProductoBase):
    id: int
    class Config:
        from_attributes = True

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    imagen: Optional[str] = None
    cantidad: Optional[int] = None
    precio: Optional[float] = None
    estado: Optional[str] = None

class Producto(ProductoBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]
    estado: str # Asegúrate de que este campo esté aquí

    class Config:
        orm_mode = True
class ActualizarCantidad(BaseModel):
    cantidad: int

class ProductoInfo(BaseModel):
    id: int
    nombre: str
    imagen: Optional[str] = None
    class Config:
        from_attributes = True

# --- Esquemas de Historial ---
class HistorialBase(BaseModel):
    bar_id: int
    mensaje: str
    tipo: str

class HistorialCreate(HistorialBase):
    producto_id: int
    pass

class HistorialOut(HistorialBase):
    id: int
    tiempo: datetime
    producto_id: Optional[int] = None
    class Config:
        from_attributes = True

class HistorialWithProduct(BaseModel):
    id: int
    bar_id: int
    producto_id: Optional[int]
    mensaje: str
    tipo: str
    tiempo: datetime
    producto_info: Optional[ProductoInfo] = None
    class Config:
        from_attributes = True

class HistorialSimpleOut(BaseModel):
    id: int
    bar_id: int
    producto_id: Optional[int]
    mensaje: str
    tipo: str
    tiempo: datetime
    class Config:
        from_attributes = True

# --- Nuevos esquemas para la Facturación ---
class DetalleFacturaInput(BaseModel):
    producto_id: int
    cantidad_final: int



class DetalleFacturaOut(BaseModel):
    id: int
    producto_id: int
    nombre_producto: str
    precio_unitario: float
    cantidad_inicial: int
    cantidad_final: int
    cantidad_vendida: int
    subtotal: float
    imagen_producto: Optional[str] = None 
    class Config:
        from_attributes = True


class GastoInput(BaseModel):
    nombre: str
    precio: float

class GastoOut(BaseModel):
    id: int
    nombre: str
    precio: float
    class Config:
        from_attributes = True
class FacturaData(BaseModel):
    id: int
    fecha: str
    hora: str
    admin_nombre: str
    total_ingresos: float
    total_gastos: float
    total_neto: float
    detalles: List[DetalleFacturaOut]
    bar_nombre: str
    gastos: List[GastoOut]

class FacturaCreateRequest(BaseModel):
    bar_id: int
    administrador_id: int
    productos: List[DetalleFacturaInput]
    gastos_hormiga: Optional[List[GastoInput]] = []

# esquemas (schemas.py)
def generate_invoice_html(invoice_data: FacturaData) -> str:
    """
    Genera el HTML para el correo de la factura con desglose de productos y gastos.
    """
    def format_price(price: float) -> str:
        """Formatea el precio con puntos como separadores de miles."""
        return f"{int(price):,}".replace(",", ".")
    
    # Determinar si hay pérdidas o no hubo ventas
    es_perdida = invoice_data.total_neto < 0
    sin_ventas = invoice_data.total_ingresos == 0
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Factura de Venta</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
            
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #000000 0%, #1a1a2e 25%, #e91e63 75%, #2196f3 100%);
                min-height: 100vh;
                padding: 20px;
                color: #333;
            }}
            
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: #ffffff;
                border-radius: 25px;
                overflow: hidden;
                box-shadow: 0 25px 50px rgba(0,0,0,0.3);
                border: 4px solid #d4af37;
                position: relative;
            }}
            
            .container::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 8px;
                background: linear-gradient(90deg, #000000, #d4af37, #e91e63, #2196f3);
            }}
            
            .header {{
                background: linear-gradient(135deg, #000000 0%, #1a1a2e 100%);
                color: white;
                text-align: center;
                padding: 40px 20px;
                position: relative;
                overflow: hidden;
            }}
            
            .header h1 {{
                font-size: 2.5em;
                font-weight: 700;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
                color: white;
                background: none;
                -webkit-background-clip: unset;
                -webkit-text-fill-color: white;
                background-clip: unset;
                position: relative;
                z-index: 1;
            }}
            
            .info-section {{
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                padding: 30px;
                border-bottom: 3px solid #d4af37;
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
            }}
            
            .info-card {{
                background: white;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);
                border-left: 5px solid #d4af37;
            }}
            
            .info-item {{
                margin: 12px 0;
                font-size: 15px;
                display: flex;
                align-items: center;
            }}
            
            .info-label {{
                font-weight: 600;
                color: #000000;
                min-width: 120px;
                margin-right: 10px;
            }}
            
            .info-value {{
                color: #2196f3;
                font-weight: 500;
            }}
            
            .products-title {{
                text-align: center;
                padding: 30px 20px 20px;
                font-size: 1.8em;
                font-weight: 600;
                color: #000000;
                background: linear-gradient(45deg, #d4af37, #f4d03f);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}

            .gastos-title {{
                text-align: center;
                padding: 20px;
                font-size: 1.8em;
                font-weight: 600;
                color: #e91e63;
            }}
            
            .product-table {{
                width: 100%;
                border-collapse: collapse;
                margin: 0 20px 30px 20px;
                width: calc(100% - 40px);
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}
            
            .product-table th {{
                background: linear-gradient(135deg, #000000 0%, #1a1a2e 100%);
                color: #d4af37;
                padding: 20px 15px;
                text-align: center;
                font-weight: 600;
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            
            .product-table td {{
                padding: 20px 15px;
                text-align: center;
                font-size: 14px;
                border-bottom: 2px solid #f0f0f0;
                transition: background-color 0.3s ease;
            }}
            
            .product-table tr:nth-child(even) td {{
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            }}
            
            .product-table tr:hover td {{
                background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            }}
            
            .product-name {{
                font-weight: 600;
                color: #000000;
                font-size: 15px;
            }}
            
            .quantity {{
                font-weight: 500;
                color: #2196f3;
            }}
            
            .price {{
                font-weight: 600;
                color: #e91e63;
                font-size: 15px;
            }}

            .summary-section {{
                padding: 40px;
                background: linear-gradient(135deg, #000000 0%, #1a1a2e 100%);
                text-align: center;
            }}

            .summary-row {{
                display: flex;
                justify-content: center;
                gap: 50px;
                margin-bottom: 30px;
                flex-wrap: wrap;
            }}

            .summary-item {{
                color: white;
                text-align: center;
                width: 250px;
            }}
            
            .summary-item .label {{
                font-size: 1.2em;
                font-weight: 500;
                letter-spacing: 1px;
                margin-bottom: 5px;
            }}
            
            .summary-item .value {{
                font-size: 2.2em;
                font-weight: 700;
            }}

            .ingresos .label {{ color: #ffffff; }}
            .ingresos .value {{ color: #2196f3; text-shadow: 1px 1px 3px rgba(33, 150, 243, 0.5); }}
            
            .gastos .label {{ color: #ffffff; }}
            .gastos .value {{ color: #e91e63; text-shadow: 1px 1px 3px rgba(233, 30, 99, 0.5); }}

            /* Estilos para Total Neto Positivo */
            .total-neto-card {{
                background: #fff;
                color: #1a1a2e;
                padding: 30px 50px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.5);
                border: 3px solid #d4af37;
                display: inline-block;
                max-width: 500px;
                width: 100%;
                margin: 0 auto;
            }}
            
            .total-neto-card .label {{
                font-size: 1.5em;
                font-weight: 600;
                color: #000000;
                margin-bottom: 10px;
            }}

            .total-neto-card .value {{
                font-size: 3.5em;
                font-weight: 700;
                color: #d4af37;
                background: linear-gradient(45deg, #d4af37, #f4d03f);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-shadow: none;
            }}

            /* Estilos para Pérdidas */
            .total-neto-card.perdida {{
                background: #fff;
                border: 3px solid #e91e63;
                box-shadow: 0 10px 30px rgba(233, 30, 99, 0.4);
            }}

            .total-neto-card.perdida .label {{
                color: #c62828;
            }}

            .total-neto-card.perdida .value {{
                color: #e91e63;
                background: linear-gradient(45deg, #e91e63, #ff6090);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}

            .alerta-perdida {{
                background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
                color: #c62828;
                padding: 20px;
                border-radius: 15px;
                margin: 20px auto;
                max-width: 600px;
                box-shadow: 0 5px 15px rgba(233, 30, 99, 0.3);
                border-left: 5px solid #e91e63;
                font-weight: 600;
                font-size: 1.1em;
                text-align: center;
            }}

            .alerta-perdida .icono {{
                font-size: 2em;
                margin-bottom: 10px;
            }}

            .alerta-sin-ventas {{
                background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
                color: #e65100;
                padding: 20px;
                border-radius: 15px;
                margin: 20px auto;
                max-width: 600px;
                box-shadow: 0 5px 15px rgba(255, 152, 0, 0.3);
                border-left: 5px solid #ff9800;
                font-weight: 600;
                font-size: 1.1em;
                text-align: center;
            }}

            .alerta-sin-ventas .icono {{
                font-size: 2em;
                margin-bottom: 10px;
            }}
            
            .footer {{
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                text-align: center;
                padding: 30px;
                color: #6c757d;
            }}
            
            .footer h3 {{
                color: #d4af37;
                font-size: 1.3em;
                margin-bottom: 10px;
                font-weight: 600;
            }}
            
            .footer p {{
                font-size: 16px;
                font-weight: 500;
            }}
            
            @media (max-width: 768px) {{
                .info-section {{
                    grid-template-columns: 1fr;
                }}
                
                .product-table {{
                    font-size: 12px;
                }}
                
                .product-table th,
                .product-table td {{
                    padding: 10px 8px;
                }}
                
                .header h1 {{
                    font-size: 2em;
                }}
                
                .summary-row {{
                    flex-direction: column;
                    gap: 30px;
                }}

                .summary-item {{
                    width: 100%;
                }}

                .total-neto-card {{
                    padding: 20px;
                }}

                .total-neto-card .value {{
                    font-size: 2.5em;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>💎 Factura de Venta 💎</h1>
            </div>
            
            <div class="info-section">
                <div class="info-card">
                    <div class="info-item">
                        <span class="info-label">🏪 Bar:</span>
                        <span class="info-value">{invoice_data.bar_nombre}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">📋 Factura:</span>
                        <span class="info-value">#{invoice_data.id}</span>
                    </div>
                </div>
                
                <div class="info-card">
                    <div class="info-item">
                        <span class="info-label">📅 Fecha:</span>
                        <span class="info-value">{invoice_data.fecha}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">🕐 Hora:</span>
                        <span class="info-value">{invoice_data.hora}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">👨‍💼 Generado por:</span>
                        <span class="info-value">{invoice_data.admin_nombre}</span>
                    </div>
                </div>
            </div>
            
            <h2 class="products-title">📦 Productos Vendidos</h2>
            
            <table class="product-table">
                <thead>
                    <tr>
                        <th>🍺 Producto</th>
                        <th>📦 Inicial</th>
                        <th>📋 Final</th>
                        <th>✅ Vendidos</th>
                        <th>💰 Precio Unit.</th>
                        <th>💎 Subtotal</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    # Detalle de cada producto con formato mejorado
    for item in invoice_data.detalles:
        html_content += f"""
        <tr>
            <td class="product-name">{item.nombre_producto}</td>
            <td class="quantity">{item.cantidad_inicial}</td>
            <td class="quantity">{item.cantidad_final}</td>
            <td class="quantity">{item.cantidad_vendida}</td>
            <td class="price">${format_price(item.precio_unitario)}</td>
            <td class="price">${format_price(item.subtotal)}</td>
        </tr>
        """
    
    html_content += f"""
                </tbody>
            </table>
    """
    
    # Sección de Gastos si existen
    if invoice_data.gastos:
        html_content += f"""
        <h2 class="gastos-title">💸 Gastos Adicionales</h2>
        <table class="product-table">
            <thead>
                <tr>
                    <th>📝 Concepto</th>
                    <th>💰 Monto</th>
                </tr>
            </thead>
            <tbody>
        """
        for gasto in invoice_data.gastos:
            html_content += f"""
                <tr>
                    <td class="product-name">{gasto.nombre}</td>
                    <td class="price">${format_price(gasto.precio)}</td>
                </tr>
            """
        html_content += f"""
            </tbody>
        </table>
        """

    # Nueva sección de totales
    html_content += f"""
            <div class="summary-section">
                <div class="summary-row">
                    <div class="summary-item ingresos">
                        <div class="label">💰 Total de Ingresos del Bar</div>
                        <div class="value">${format_price(invoice_data.total_ingresos)}</div>
                    </div>
                    <div class="summary-item gastos">
                        <div class="label">💸 Total de Gastos</div>
                        <div class="value">-${format_price(invoice_data.total_gastos)}</div>
                    </div>
                </div>
    """
    
    # Alerta de pérdida si el total neto es negativo
    if sin_ventas:
        html_content += f"""
                <div class="alerta-sin-ventas">
                    <div class="icono">🚫</div>
                    <div>No se registraron ventas durante el día</div>
                </div>
        """
    elif es_perdida:
        html_content += f"""
                <div class="alerta-perdida">
                    <div class="icono">⚠️</div>
                    <div>¡ATENCIÓN! El día ha cerrado con pérdidas</div>
                </div>
        """
    
    # Card del total neto con clase condicional
    if sin_ventas:
        clase_perdida = ""
        emoji_total = "🚫"
        label_total = "Sin Ventas del Día"
    elif es_perdida:
        clase_perdida = "perdida"
        emoji_total = "📉"
        label_total = "Pérdida del Día"
    else:
        clase_perdida = ""
        emoji_total = "✨"
        label_total = "Total Neto del Día"
    
    html_content += f"""
                <div class="total-neto-card {clase_perdida}">
                    <div class="label">{emoji_total} {label_total} {emoji_total}</div>
                    <div class="value">${format_price(invoice_data.total_neto)}</div>
                </div>
            </div>
            
            <div class="footer">
                <h3>Control AS</h3>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content
# Esquema de salida para la factura completa con info del admin
class FacturaOut(BaseModel):
    id: int
    fecha: date
    hora: datetime
    administrador_id: int
    bar_id: int
    total_ingresos: float
    
    # ✅ Nuevos campos para los gastos y totales netos
    total_gastos: float
    total_neto: float
    gastos: List[GastoOut]
    
    # 📦 Relación con los detalles de los productos
    detalles_factura: List[DetalleFacturaOut]
    
    # 🎯 Campos para la información del administrador
    admin_nombre: Optional[str] = None
    admin_foto: Optional[str] = None

    class Config:
        from_attributes = True

# app/schemas.py (continúa)
class HistorialEmailItem(BaseModel):
    mensaje: str
    tiempo: datetime
    tipo: str
    class Config:
        from_attributes = True

# Faltaba un espacio y nueva línea aquí
class HistorialEmailData(BaseModel):
    bar_nombre: str
    fecha_borrado: str
    historial: List[HistorialEmailItem]


def generate_history_html(history_data: HistorialEmailData) -> str:
    """Genera el HTML para el correo del historial eliminado."""
    
    # Mapeo de tipos de historial a clases de CSS
    color_map = {
        "elimino": "message-elimino",
        "agrego": "message-agrego",
        "aumento": "message-aumento",
        "disminuyo": "message-disminuyo"
    }

    # Genera los ítems del historial con la clase de estilo correcta
    history_items_html = ""
    for item in history_data.historial:
        # Usa el mapa para obtener la clase, por defecto usa una clase neutral si no coincide
        css_class = color_map.get(item.tipo, "history-item-default")
        
        history_items_html += f"""
        <div class="history-item {css_class}">
            <div class="item-message">{item.mensaje}</div>
            <div class="item-info">Tipo: {item.tipo} | Fecha y hora: {item.tiempo.strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
        """
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; color: #333; margin: 0; padding: 0; }}
            .container {{ max-width: 600px; margin: 20px auto; background-color: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border-top: 5px solid #007bff; }}
            .header {{ text-align: center; margin-bottom: 20px; }}
            .header h1 {{ color: #007bff; font-size: 24px; }}
            .header p {{ color: #666; font-size: 14px; }}
            .content {{ margin-bottom: 20px; }}
            .content h2 {{ color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 20px; }}
            .history-item {{ background-color: #f8f9fa; border-left: 3px solid; padding: 15px; border-radius: 5px; margin-bottom: 10px; }}
            .item-message {{ font-weight: bold; margin-bottom: 5px; }}
            .item-info {{ font-size: 12px; color: #888; }}
            .footer {{ text-align: center; margin-top: 30px; font-size: 12px; color: #999; }}
            
            /* Clases de estilo para los nuevos tipos de mensaje */
            .message-elimino {{ border-color: #dc3545; }} /* Rojo */
            .message-agrego {{ border-color: #28a745; }} /* Verde */
            .message-aumento {{ border-color: #007bff; }} /* Azul */
            .message-disminuyo {{ border-color: #e83e8c; }} /* Rosa */
            .history-item-default {{ border-color: #6c757d; }} /* Gris por defecto */
            
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Historial de Nevera Eliminado 🗑️</h1>
                <p>Copia de seguridad del historial del bar <strong>{history_data.bar_nombre}</strong></p>
                <p>Fecha de borrado: {history_data.fecha_borrado}</p>
            </div>
            <div class="content">
                <h2>Detalles del Historial</h2>
                {history_items_html}
            </div>
            <div class="footer">
                <p>Este correo se generó automáticamente al eliminar el historial de su nevera.</p>
                <p>
Control AS Bar. Todos los derechos reservados.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content


class ForgotPasswordRequest(BaseModel):
    correo: str

class ResetPasswordRequest(BaseModel):
    token: str
    nueva_contraseña: str


# ==== NUEVOS ESQUEMAS PARA TAREAS COMPLETADAS ====
class TareaCompletadaItem(BaseModel):
    descripcion: str
    fecha: date
    fecha_completada: Optional[date] = None

    class Config:
        from_attributes = True

class TareasEmailData(BaseModel):
    bar_nombre: str
    administrador_nombre: str
    mes_anterior: str  # ej: "Octubre 2025"
    tareas: List[TareaCompletadaItem]

class ResumenDuenoData(BaseModel):
    bar_nombre: str
    mes_anterior: str
    administradores: List[TareasEmailData]

def generate_tareas_admin_html(data: TareasEmailData) -> str:
    """HTML bonito para el correo del administrador"""
    total = len(data.tareas)
    html_tareas = ""
    for t in data.tareas:
        fecha_comp = t.fecha_completada.strftime("%d/%m/%Y") if t.fecha_completada else "No registrada"
        html_tareas += f"""
        <tr>
            <td style="padding: 12px; border-bottom: 1px solid #eee; text-align: left;">{t.descripcion}</td>
            <td style="padding: 12px; border-bottom: 1px solid #eee; text-align: center;">{t.fecha.strftime('%d/%m/%Y')}</td>
            <td style="padding: 12px; border-bottom: 1px solid #eee; text-align: center; color: #28a745; font-weight: 600;">✓ {fecha_comp}</td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background: #f4f4f9; padding: 20px; }}
            .container {{ max-width: 700px; margin: auto; background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 20px; text-align: center; }}
            .header h1 {{ margin: 0; font-size: 28px; }}
            .content {{ padding: 30px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th {{ background: #667eea; color: white; padding: 15px; }}
            .footer {{ background: #f8f9fa; padding: 20px; text-align: center; color: #666; font-size: 14px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>✨ Tareas Completadas - {data.mes_anterior}</h1>
                <p>Bar: <strong>{data.bar_nombre}</strong></p>
            </div>
            <div class="content">
                <p>Hola <strong>{data.administrador_nombre}</strong> 👋</p>
                <p>¡Excelente trabajo! Durante <strong>{data.mes_anterior}</strong> completaste <strong>{total}</strong> tarea(s):</p>
                <table>
                    <thead>
                        <tr>
                            <th>Descripción</th>
                            <th>Fecha Asignada</th>
                            <th>Completada</th>
                        </tr>
                    </thead>
                    <tbody>
                        {html_tareas}
                    </tbody>
                </table>
                <p>¡Sigue así! 💪</p>
            </div>
            <div class="footer">
                <p>Control AS • Resumen mensual automático</p>
            </div>
        </div>
    </body>
    </html>
    """

def generate_resumen_dueno_html(data: ResumenDuenoData) -> str:
    """HTML bonito para el correo del dueño (resumen de todos los admins)"""
    total_tareas = sum(len(admin.tareas) for admin in data.administradores)
    admins_html = ""
    for admin in data.administradores:
        admins_html += f"""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #667eea;">
            <h3 style="margin: 0 0 10px 0; color: #333;">👤 {admin.administrador_nombre}</h3>
            <p><strong>{len(admin.tareas)}</strong> tareas completadas</p>
            <ul style="margin: 10px 0; padding-left: 20px;">
                {''.join(f"<li>{t.descripcion} <small>(completada el {t.fecha_completada.strftime('%d/%m/%Y') if t.fecha_completada else '??'})</small></li>" for t in admin.tareas)}
            </ul>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background: #f0f2f5; padding: 20px; }}
            .container {{ max-width: 800px; margin: auto; background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.15); }}
            .header {{ background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; padding: 40px; text-align: center; }}
            .header h1 {{ margin: 0; font-size: 30px; }}
            .content {{ padding: 40px; }}
            .total {{ font-size: 24px; text-align: center; background: #38ef7d; color: white; padding: 20px; border-radius: 10px; margin-bottom: 30px; }}
            .footer {{ background: #f8f9fa; padding: 25px; text-align: center; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Resumen Mensual de Tareas Completadas</h1>
                <p>Bar: <strong>{data.bar_nombre}</strong> • {data.mes_anterior}</p>
            </div>
            <div class="content">
                <div class="total">
                    ¡En total se completaron <strong>{total_tareas}</strong> tareas este mes! 🎉
                </div>
                {admins_html or "<p>No hubo tareas completadas este mes.</p>"}
            </div>
            <div class="footer">
                <p>Control AS • Reporte automático mensual • {datetime.now().strftime('%d/%m/%Y')}</p>
            </div>
        </div>
    </body>
    </html>
    """
def get_password_hash(password: str) -> Any:
    contexto_local = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    # 2. Devolver el hash
    return contexto_local.hash(password)
# --- Esquemas de Login ---

class GestorPrincipalLoginRequest(BaseModel):

    correo: str
    contraseña: str

# El esquema de respuesta solo contiene los campos de la tabla.
class GestorPrincipalLoginResponse(BaseModel):

    id: int
    nombre: str
    correo: str

    class Config:
        from_attributes = True


class DuenoUpdate(BaseModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    cantidad_bares: Optional[int] = None 
    estado: Optional[str] = None
    imagen: Optional[str] = None

class VerifyCodeRequest(BaseModel):
    token: str