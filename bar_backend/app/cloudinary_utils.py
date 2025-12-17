# app/cloudinary_utils.py - VERSIÓN FINAL OPTIMIZADA CON CARPETAS POR BAR
import cloudinary
import cloudinary.uploader
import cloudinary.api
import base64
from io import BytesIO

# ✅ CONFIGURACIÓN CENTRALIZADA DE CLOUDINARY
# (Ya no se duplica, se carga una sola vez)
cloudinary.config(
    cloud_name="dymgfvafu",
    api_key="784682236934985",
    api_secret="wR1U8ycWCJp6V9KQheeFwpgs9Gs",
    secure=True
)


def subir_imagen_a_cloudinary(imagen_base64: str, carpeta: str = "otros", bar_id: int = None) -> str:
    """
    Sube una imagen en base64 a Cloudinary dentro de la carpeta 'controlas/[carpeta]'.
    Si es un producto Y se proporciona bar_id, usa carpeta 'controlas/productos/bar_{bar_id}'
    De lo contrario usa 'controlas/{carpeta}'
    Si ya es una URL, la devuelve tal cual.
    Default: carpeta "otros" si no se especifica.
    
    Args:
        imagen_base64: Imagen en formato base64 o URL
        carpeta: Nombre de la carpeta (duenos, bares, productos, administradores, mujeres, etc)
        bar_id: ID del bar (opcional, solo para productos)
    
    Returns:
        URL de la imagen en Cloudinary o None si falla
    """
    print(f"\n{'='*70}")
    print(f"☁️ SUBIENDO IMAGEN A CLOUDINARY")
    print(f"📁 Carpeta solicitada: {carpeta}")
    if bar_id:
        print(f"🏪 Bar ID: {bar_id}")
    print(f"{'='*70}")

    if not imagen_base64:
        print("⚠️ IMAGEN VACÍA O NONE → Retornando None")
        return None

    print(f"📏 Longitud base64: {len(imagen_base64)} caracteres")
    print(f"🔍 Inicio: {imagen_base64[:60]}...")

    # Si ya es URL de Cloudinary o externa → no subir
    if imagen_base64.startswith("http"):
        print(f"↩️ YA ES UNA URL → No se sube")
        print(f"🔗 URL existente: {imagen_base64}")
        return imagen_base64

    # CARPETA ESPECÍFICA PARA PRODUCTOS POR BAR (optimización de búsquedas)
    if carpeta == "productos" and bar_id:
        folder_path = f"controlas/productos/bar_{bar_id}"
        print(f"🎯 Carpeta específica del bar: {folder_path}")
    else:
        # Para otras entidades: duenos, bares, administradores, mujeres, etc.
        carpeta_final = carpeta.strip() if carpeta else "otros"
        folder_path = f"controlas/{carpeta_final}"

    try:
        print(f"🚀 Subiendo a: {folder_path}")
        resultado = cloudinary.uploader.upload(
            imagen_base64,
            folder=folder_path,
            use_filename=True,
            unique_filename=True,   # Evita nombres duplicados
            overwrite=False,        # No sobrescribe si ya existe (seguro)
            resource_type="image"
        )

        url_final = resultado["secure_url"]
        public_id = resultado.get("public_id", "N/A")

        print(f"✅ ¡SUBIDA EXITOSA!")
        print(f"🔗 URL: {url_final}")
        print(f"📦 Public ID: {public_id}")
        print(f"📏 Tamaño: {resultado.get('bytes', 0) / 1024:.2f} KB")
        print(f"{'='*70}\n")

        return url_final

    except Exception as e:
        print(f"❌ ERROR AL SUBIR IMAGEN:")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Mensaje: {str(e)}")
        print(f"⚠️ FALLBACK → Guardando base64 original")
        print(f"{'='*70}\n")
        return imagen_base64


def subir_pdf_a_cloudinary(archivo_binario: bytes, nombre_archivo: str) -> dict:
    """
    Sube un PDF a la carpeta controlas/facturas_inventario
    
    Args:
        archivo_binario: Contenido del archivo PDF en bytes
        nombre_archivo: Nombre del archivo PDF
    
    Returns:
        Diccionario con url, nombre y mime_type o None si falla
    """
    print(f"\n{'='*70}")
    print(f"📄 SUBIENDO PDF: {nombre_archivo}")
    print(f"{'='*70}")

    if not archivo_binario:
        print("⚠️ ARCHIVO VACÍO → Retornando None")
        return None

    print(f"📏 Tamaño: {len(archivo_binario) / 1024:.2f} KB")

    try:
        resultado = cloudinary.uploader.upload(
            archivo_binario,
            folder="controlas/facturas_inventario",
            public_id=nombre_archivo.split('.')[0],
            resource_type="raw",
            overwrite=True
        )

        url_final = resultado["secure_url"]

        print(f"✅ PDF SUBIDO CORRECTAMENTE")
        print(f"🔗 URL: {url_final}")
        print(f"{'='*70}\n")

        return {
            "url": url_final,
            "nombre": nombre_archivo,
            "mime_type": "application/pdf"
        }

    except Exception as e:
        print(f"❌ ERROR SUBIENDO PDF:")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Mensaje: {str(e)}")
        print(f"{'='*70}\n")
        return None


def eliminar_imagen_de_cloudinary(url_imagen: str) -> bool:
    """
    Elimina una imagen de Cloudinary usando su URL pública.
    Devuelve True si se borró exitosamente, False si no existía o hubo error.
    
    Args:
        url_imagen: URL completa de la imagen en Cloudinary
    
    Returns:
        True si se eliminó correctamente, False en caso contrario
    """
    if not url_imagen or not url_imagen.startswith("https://res.cloudinary.com/dymgfvafu"):
        print(f"⚠️ URL no válida para borrado: {url_imagen[:60] if url_imagen else 'None'}...")
        return False

    try:
        # Extraer public_id de la URL
        # Formato: https://res.cloudinary.com/dymgfvafu/image/upload/v123456/controlas/carpeta/archivo.jpg
        partes = url_imagen.split("/upload/")
        if len(partes) < 2:
            print("⚠️ Formato de URL inesperado")
            return False

        public_id_con_version = partes[1]
        public_id = public_id_con_version.split("?")[0]  # Quitar parámetros query
        public_id = public_id.rsplit(".", 1)[0]  # Quitar extensión (.jpg, .png, etc)

        print(f"🗑️ Eliminando imagen: {public_id}")

        resultado = cloudinary.uploader.destroy(public_id, resource_type="image")

        if resultado.get("result") == "ok":
            print(f"✅ Imagen borrada exitosamente: {public_id}")
            return True
        elif resultado.get("result") == "not found":
            print(f"ℹ️ Imagen ya no existía: {public_id}")
            return False
        else:
            print(f"⚠️ Respuesta inesperada: {resultado}")
            return False

    except Exception as e:
        print(f"❌ Error borrando imagen: {e}")
        return False


def eliminar_pdf_de_cloudinary(url_pdf: str) -> bool:
    """
    Elimina un PDF de Cloudinary usando su URL pública.
    Similar a eliminar_imagen_de_cloudinary pero para archivos tipo 'raw'.
    
    Args:
        url_pdf: URL completa del PDF en Cloudinary
    
    Returns:
        True si se eliminó correctamente, False en caso contrario
    """
    if not url_pdf or not url_pdf.startswith("https://res.cloudinary.com/dymgfvafu"):
        print(f"⚠️ URL de PDF no válida para borrado: {url_pdf[:60] if url_pdf else 'None'}...")
        return False

    try:
        # Extraer public_id de la URL
        partes = url_pdf.split("/upload/")
        if len(partes) < 2:
            print("⚠️ Formato de URL de PDF inesperado")
            return False

        public_id_con_version = partes[1]
        public_id = public_id_con_version.split("?")[0]  # Quitar parámetros
        # No quitamos la extensión .pdf porque es necesaria para archivos raw

        print(f"🗑️ Eliminando PDF: {public_id}")

        resultado = cloudinary.uploader.destroy(public_id, resource_type="raw")

        if resultado.get("result") == "ok":
            print(f"✅ PDF borrado exitosamente: {public_id}")
            return True
        elif resultado.get("result") == "not found":
            print(f"ℹ️ PDF ya no existía: {public_id}")
            return False
        else:
            print(f"⚠️ Respuesta inesperada al borrar PDF: {resultado}")
            return False

    except Exception as e:
        print(f"❌ Error borrando PDF: {e}")
        return False


def eliminar_carpeta_completa(carpeta_path: str) -> dict:
    """
    Elimina una carpeta completa de Cloudinary con todas sus imágenes.
    Útil para eliminar todas las imágenes de un bar específico.
    
    Args:
        carpeta_path: Ruta de la carpeta (ej: "controlas/productos/bar_5")
    
    Returns:
        Diccionario con resultados de la operación
    """
    print(f"\n{'='*70}")
    print(f"🗑️ ELIMINANDO CARPETA COMPLETA: {carpeta_path}")
    print(f"{'='*70}")

    try:
        # Listar todos los recursos en la carpeta
        resultado = cloudinary.api.delete_resources_by_prefix(carpeta_path)
        
        deleted_count = len(resultado.get('deleted', {}))
        
        print(f"✅ Carpeta eliminada: {deleted_count} archivos borrados")
        print(f"{'='*70}\n")
        
        return {
            "success": True,
            "deleted_count": deleted_count,
            "carpeta": carpeta_path
        }
        
    except Exception as e:
        print(f"❌ Error eliminando carpeta: {e}")
        print(f"{'='*70}\n")
        return {
            "success": False,
            "error": str(e),
            "carpeta": carpeta_path
        }