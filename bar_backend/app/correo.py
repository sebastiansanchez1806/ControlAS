import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv
from pathlib import Path

# --- Bloque de Carga de Variables de Entorno (sin cambios) ---
# Buscar el archivo correo.env en múltiples ubicaciones
env_paths = [
    Path("correo.env"),
    Path(__file__).parent / "correo.env",
    Path(__file__).parent.parent / "correo.env",
]

env_loaded = False
for env_path in env_paths:
    if env_path.exists():
        print(f"📁 Cargando variables de entorno desde: {env_path.absolute()}")
        load_dotenv(env_path)
        env_loaded = True
        break

if not env_loaded:
    print("⚠️ No se encontró el archivo correo.env, intentando cargar desde .env")
    load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))

print(f"🔍 EMAIL_USER cargado: {'✅ Sí' if EMAIL_USER else '❌ No'}")
print(f"🔍 EMAIL_PASS cargado: {'✅ Sí' if EMAIL_PASS else '❌ No'}")
print(f"🔍 EMAIL_HOST: {EMAIL_HOST}")
print(f"🔍 EMAIL_PORT: {EMAIL_PORT}")

if not EMAIL_USER or not EMAIL_PASS:
    print("⚠️ Usando credenciales directas como fallback")
    EMAIL_USER = "migracionessenacba@gmail.com"
    EMAIL_PASS = "ovng wffn yjok ajuf"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587

# --- Función Corregida para Responsividad ---

def generar_html_tarea(admin_nombre: str, descripcion: str, fecha: str, bar_nombre: str = None, dueno_nombre: str = None) -> str:
    """Genera el HTML para el correo de notificación de tarea (Responsive)"""
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Nueva Tarea Asignada</title>
        <style>
            body {{ margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0a0a0a; }}
            /* Media query para hacer el contenedor full width en móviles */
            @media screen and (max-width: 620px) {{
                /* Aplica el ancho máximo solo cuando es menor a 620px */
                .container-table {{ width: 100% !important; max-width: 100% !important; border-radius: 0 !important; }}
                /* Ajusta el padding para móviles */
                .main-td {{ padding: 20px 10px !important; }}
                .content-td {{ padding: 25px 20px !important; }}
                .header-td {{ padding: 40px 20px !important; }}
                h1 {{ font-size: 30px !important; }}
                h2 {{ font-size: 20px !important; }}
            }}
        </style>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0a0a0a;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #0a0a0a;">
            <tr>
                <td align="center" class="main-td" style="padding: 40px 20px;">
                    <table class="container-table" width="100%" cellpadding="0" cellspacing="0" 
                           style="max-width: 600px; width: 100%; background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%); border-radius: 24px; overflow: hidden; box-shadow: 0 20px 60px rgba(233, 30, 99, 0.3);">
                        
                        <tr>
                            <td style="height: 4px; background: linear-gradient(90deg, #e91e63, #2196f3, #e91e63);"></td>
                        </tr>
                        
                        <tr>
                            <td class="header-td" style="background: linear-gradient(135deg, #000000 0%, #1a1a2e 50%, #e91e63 100%); padding: 50px 30px; text-align: center;">
                                <div style="font-size: 64px; margin-bottom: 20px;">✨</div>
                                <h1 style="margin: 0; font-size: 36px; font-weight: 800; color: #ffffff; letter-spacing: 1px;">Nueva Tarea Asignada</h1>
                                <p style="margin: 10px 0 0 0; color: rgba(255, 255, 255, 0.7); font-size: 16px;">Tienes una nueva responsabilidad</p>
                            </td>
                        </tr>
                        
                        <tr>
                            <td class="content-td" style="padding: 40px 35px; background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%);">
                                
                                <h2 style="margin: 0 0 20px 0; font-size: 24px; font-weight: 700; color: #ffffff;">¡Hola {admin_nombre}! 👋</h2>
                                
                                <p style="margin: 0 0 35px 0; font-size: 16px; line-height: 1.8; color: rgba(255, 255, 255, 0.85);">
                                    {"<strong style='color: #e91e63;'>" + dueno_nombre + "</strong>" if dueno_nombre else "El dueño del bar"} te ha asignado una nueva tarea. Revisa los detalles a continuación y asegúrate de completarla antes de la fecha indicada.
                                </p>
                                
                                {f'''<table width="100%" cellpadding="0" cellspacing="0" style="background: linear-gradient(135deg, rgba(233, 30, 99, 0.15), rgba(33, 150, 243, 0.15)); border-left: 4px solid #e91e63; border-radius: 12px; margin-bottom: 30px;">
                                    <tr>
                                        <td style="padding: 18px 22px;">
                                            <table cellpadding="0" cellspacing="0">
                                                <tr>
                                                    <td style="font-size: 28px; padding-right: 12px; vertical-align: middle;">👨‍💼</td>
                                                    <td style="vertical-align: middle;">
                                                        <div style="font-size: 13px; color: rgba(255, 255, 255, 0.6); margin-bottom: 4px;">ASIGNADO POR</div>
                                                        <div style="font-size: 19px; font-weight: 700; color: #e91e63;">{dueno_nombre}</div>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>''' if dueno_nombre else ''}
                                
                                <table width="100%" cellpadding="0" cellspacing="0" style="background: linear-gradient(135deg, rgba(233, 30, 99, 0.1) 0%, rgba(33, 150, 243, 0.1) 100%); border: 2px solid rgba(233, 30, 99, 0.3); border-radius: 16px; margin: 25px 0;">
                                    
                                    <tr>
                                        <td colspan="2" style="height: 3px; background: linear-gradient(90deg, #e91e63, #2196f3, #e91e63);"></td>
                                    </tr>
                                    
                                    <tr>
                                        <td colspan="2" style="padding: 30px 30px 0 30px;">
                                            <table cellpadding="0" cellspacing="0" width="100%">
                                                <tr>
                                                    <td style="font-size: 32px; width: 50px; text-align: center; vertical-align: top;">🏪</td>
                                                    <td style="vertical-align: top; padding-bottom: 20px; border-bottom: 1px solid rgba(255, 255, 255, 0.1);">
                                                        <div style="font-size: 14px; color: rgba(255, 255, 255, 0.5); font-weight: 500; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 0.5px;">LOCAL</div>
                                                        <div style="font-size: 18px; color: #2196f3; font-weight: 600;">{bar_nombre if bar_nombre else 'No especificado'}</div>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    
                                    <tr>
                                        <td colspan="2" style="padding: 20px 30px 0 30px;">
                                            <table cellpadding="0" cellspacing="0" width="100%">
                                                <tr>
                                                    <td style="font-size: 32px; width: 50px; text-align: center; vertical-align: top;">📅</td>
                                                    <td style="vertical-align: top; padding-bottom: 20px; border-bottom: 1px solid rgba(255, 255, 255, 0.1);">
                                                        <div style="font-size: 14px; color: rgba(255, 255, 255, 0.5); font-weight: 500; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 0.5px;">FECHA</div>
                                                        <div style="font-size: 18px; color: #e91e63; font-weight: 600;">{fecha}</div>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    
                                    <tr>
                                        <td colspan="2" style="padding: 25px 30px 30px 30px;">
                                            <div style="background: rgba(0, 0, 0, 0.3); border: 1px solid rgba(233, 30, 99, 0.3); padding: 25px; border-radius: 12px;">
                                                <div style="font-size: 14px; color: rgba(255, 255, 255, 0.5); font-weight: 600; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.5px;">📝 DESCRIPCIÓN DE LA TAREA</div>
                                                <div style="font-size: 16px; line-height: 1.7; color: rgba(255, 255, 255, 0.9);">{descripcion}</div>
                                            </div>
                                        </td>
                                    </tr>
                                </table>
                                
                                <table width="100%" cellpadding="0" cellspacing="0" style="background: linear-gradient(135deg, rgba(255, 193, 7, 0.2), rgba(255, 152, 0, 0.2)); border-left: 4px solid #ffc107; border-radius: 12px; margin: 25px 0;">
                                    <tr>
                                        <td style="padding: 20px 25px;">
                                            <table cellpadding="0" cellspacing="0">
                                                <tr>
                                                    <td style="font-size: 32px; padding-right: 15px; vertical-align: middle;">⚡</td>
                                                    <td style="color: #ffc107; font-weight: 600; font-size: 15px; vertical-align: middle;">
                                                        Recuerda completar esta tarea y marcarla en el aplicativo CONTROL AS como finalizada.
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                                
                            </td>
                        </tr>
                        
                        <tr>
                            <td style="background: #000000; text-align: center; padding: 40px 30px; border-top: 1px solid rgba(255, 255, 255, 0.1);">
                                <div style="font-size: 32px; font-weight: 900; color: #ffffff; margin-bottom: 10px; letter-spacing: 3px;">
                                    <span style="background: linear-gradient(135deg, #e91e63, #2196f3); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">CONTROL AS</span>
                                </div>
                                <div style="color: rgba(255, 255, 255, 0.5); font-size: 14px;">Sistema de Gestión Empresarial</div>
                            </td>
                        </tr>
                        
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    return html_content

# --- Bloque de Función de Envío de Email (sin cambios) ---

def enviar_email_tarea(destinatario: str, admin_nombre: str, descripcion: str, fecha: str, bar_nombre: str = None, dueno_nombre: str = None):
    """
    Envía un correo electrónico al administrador notificando sobre una nueva tarea asignada.
    
    Args:
        destinatario: Email del administrador
        admin_nombre: Nombre del administrador
        descripcion: Descripción de la tarea
        fecha: Fecha límite de la tarea
        bar_nombre: Nombre del bar (opcional)
        dueno_nombre: Nombre del dueño que asignó la tarea (opcional)
    """
    server = None
    try:
        if not EMAIL_USER or not EMAIL_PASS:
            raise ValueError("Las credenciales de email no están configuradas correctamente")
        
        print(f"🔄 Intentando enviar email a {destinatario}...")
        print(f"📧 Usando servidor: {EMAIL_HOST}:{EMAIL_PORT}")
        
        mensaje = MIMEMultipart("alternative")
        mensaje["Subject"] = f"✨ Nueva Tarea Asignada - {fecha}"
        mensaje["From"] = EMAIL_USER
        mensaje["To"] = destinatario
        
        html_content = generar_html_tarea(admin_nombre, descripcion, fecha, bar_nombre, dueno_nombre)
        
        parte_html = MIMEText(html_content, "html")
        mensaje.attach(parte_html)
        
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT, timeout=30)
        server.ehlo()
        
        print("🔐 Iniciando conexión TLS...")
        server.starttls()
        server.ehlo()
        
        print("🔑 Autenticando...")
        server.login(EMAIL_USER, EMAIL_PASS)
        
        print("📤 Enviando mensaje...")
        server.send_message(mensaje)
        
        print(f"✅ Email de tarea enviado exitosamente a {destinatario}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Error de autenticación: {str(e)}")
        print("💡 Verifica que la contraseña de aplicación sea correcta")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ Error SMTP: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error al enviar email de tarea: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False
    finally:
        if server:
            try:
                server.quit()
            except:
                pass