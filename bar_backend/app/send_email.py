# app/send_email.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo "correo.env"
# ¡Este es el cambio clave para que funcione!
# Carga las variables de entorno desde la ruta correcta
load_dotenv('app/correo.env')

# Configuración del correo desde el archivo .env
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_HOST = os.getenv("EMAIL_HOST")

# Asegúrate de que la variable existe antes de intentar convertirla a int
email_port_str = os.getenv("EMAIL_PORT")
if email_port_str is not None:
    EMAIL_PORT = int(email_port_str)
else:
    # Puedes manejar el error aquí, por ejemplo, asignando un valor por defecto
    # o levantando una excepción para que el programa se detenga
    raise ValueError("La variable de entorno 'EMAIL_PORT' no está definida en 'correo.env'.")

def send_email(to_email: str, subject: str, html_content: str):
    """
    Función para enviar un correo electrónico con contenido HTML.
    ... (El resto de la función es el mismo)
    """
    if not all([EMAIL_USER, EMAIL_PASS, EMAIL_HOST]):
        print("Error: Variables de entorno de correo no configuradas correctamente.")
        return

    # ... (El resto de tu función send_email)

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, to_email, msg.as_string())
        print(f"✅ Correo enviado a {to_email} con éxito.")
    except Exception as e:
        print(f"❌ Error al enviar el correo a {to_email}: {e}")