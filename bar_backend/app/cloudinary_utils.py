# app/cloudinary_utils.py - VERSIÓN CON LOGS DETALLADOS
import cloudinary
import cloudinary.uploader
import base64
from io import BytesIO

# ✅ CONFIGURAR CLOUDINARY
cloudinary.config(
    cloud_name="dymgfvafu",
    api_key="784682236934985",
    api_secret="wR1U8ycWCJp6V9KQheeFwpgs9Gs",
    secure=True
)

def subir_imagen_a_cloudinary(imagen_base64: str, carpeta: str = "controlas") -> str:
    """
    Sube una imagen en base64 a Cloudinary y devuelve la URL pública.
    Si ya es una URL externa, la devuelve tal cual.
    """
    print(f"\n{'='*60}")
    print(f"🔍 SUBIR IMAGEN A CLOUDINARY - Carpeta: {carpeta}")
    print(f"{'='*60}")
    
    if not imagen_base64:
        print("⚠️ NO SE RECIBIÓ IMAGEN (None o vacío)")
        return None
    
    # Log del tamaño
    print(f"📏 Tamaño recibido: {len(imagen_base64)} caracteres")
    print(f"🔍 Primeros 60 caracteres: {imagen_base64[:60]}...")
    
    # Si ya es una URL (ya subida antes o externa), no subir de nuevo
    if imagen_base64.startswith("http") or imagen_base64.startswith("https"):
        print(f"↩️ YA ES UNA URL - No se sube de nuevo")
        print(f"🔗 URL: {imagen_base64}")
        return imagen_base64
    
    try:
        print(f"☁️ Subiendo a Cloudinary...")
        print(f"📁 Carpeta destino: controlas/{carpeta}")
        
        resultado = cloudinary.uploader.upload(
            imagen_base64,
            folder=f"controlas/{carpeta}",
            use_filename=True,
            unique_filename=True,  # ← Cambiado a True para evitar sobrescrituras
            overwrite=False,        # ← No sobrescribir archivos existentes
            resource_type="image"
        )
        
        url_final = resultado["secure_url"]
        
        print(f"✅ SUBIDA EXITOSA")
        print(f"🔗 URL: {url_final}")
        print(f"📦 Public ID: {resultado.get('public_id', 'N/A')}")
        print(f"📏 Tamaño: {resultado.get('bytes', 0) / 1024:.2f} KB")
        print(f"{'='*60}\n")
        
        return url_final
        
    except Exception as e:
        print(f"❌ ERROR SUBIENDO A CLOUDINARY:")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Mensaje: {str(e)}")
        print(f"⚠️ FALLBACK: Guardando base64 original")
        print(f"{'='*60}\n")
        return imagen_base64  # Fallback: devuelve el base64 original

def subir_pdf_a_cloudinary(archivo_binario: bytes, nombre_archivo: str) -> dict:
    """
    Sube un PDF binario a Cloudinary y devuelve info con URL
    """
    print(f"\n{'='*60}")
    print(f"📄 SUBIR PDF A CLOUDINARY - Archivo: {nombre_archivo}")
    print(f"{'='*60}")
    
    if not archivo_binario:
        print("⚠️ NO SE RECIBIÓ ARCHIVO (None o vacío)")
        return None
    
    print(f"📏 Tamaño del PDF: {len(archivo_binario) / 1024:.2f} KB")
    
    try:
        print(f"☁️ Subiendo PDF...")
        
        resultado = cloudinary.uploader.upload(
            archivo_binario,
            folder="controlas/facturas_inventario",
            public_id=nombre_archivo.split('.')[0],
            resource_type="raw",
            overwrite=True
        )
        
        url_final = resultado["secure_url"]
        
        print(f"✅ PDF SUBIDO EXITOSAMENTE")
        print(f"🔗 URL: {url_final}")
        print(f"{'='*60}\n")
        
        return {
            "url": url_final,
            "nombre": nombre_archivo,
            "mime_type": "application/pdf"
        }
        
    except Exception as e:
        print(f"❌ ERROR SUBIENDO PDF:")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Mensaje: {str(e)}")
        print(f"{'='*60}\n")
        return None

# === PRUEBA DE CONEXIÓN (ejecutar al importar el módulo) ===
print("\n" + "="*60)
print("🔍 Probando conexión con Cloudinary...")
print("="*60)
try:
    test = cloudinary.uploader.upload(
        "https://upload.wikimedia.org/wikipedia/commons/a/ae/Olympic_flag.jpg",
        folder="controlas/prueba"
    )
    print(f"✅ ¡Cloudinary conectado correctamente!")
    print(f"🔗 URL de prueba: {test['secure_url']}")
    print("="*60 + "\n")
except Exception as e:
    print(f"⚠️ ADVERTENCIA: No se pudo conectar con Cloudinary")
    print(f"❌ Error: {e}")
    print("El sistema usará almacenamiento base64 como respaldo")
    print("="*60 + "\n")