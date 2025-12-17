# app/cloudinary_utils.py - VERSIÓN FINAL OPTIMIZADA
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

def subir_imagen_a_cloudinary(imagen_base64: str, carpeta: str = "otros") -> str:
    """
    Sube una imagen en base64 a Cloudinary dentro de la carpeta 'controlas/[carpeta]'.
    Si ya es una URL, la devuelve tal cual.
    Default: carpeta "otros" si no se especifica.
    """
    print(f"\n{'='*70}")
    print(f"☁️ SUBIENDO IMAGEN A CLOUDINARY")
    print(f"📁 Carpeta solicitada: {carpeta}")
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

    # Forzar carpeta dentro de controlas/
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
    Devuelve True si se borró, False si no existía o error.
    """
    if not url_imagen or not url_imagen.startswith("https://res.cloudinary.com/dymgfvafu"):
        print(f"⚠️ URL no válida para borrado: {url_imagen[:60] if url_imagen else 'None'}...")
        return False

    try:
        # Extraer public_id de la URL
        partes = url_imagen.split("/upload/")
        if len(partes) < 2:
            print("⚠️ Formato de URL inesperado")
            return False

        public_id_con_version = partes[1]
        public_id = public_id_con_version.split("?")[0]  # Quitar parámetros
        public_id = public_id.rsplit(".", 1)[0]  # Quitar extensión

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