# 🍸 ControlAS Bar - Sistema Integral de Gestión para Bares y Discotecas

**Proyecto en producción real** — Actualmente optimiza la operación diaria de **6 establecimientos** en Bogotá, entregando control total sobre inventario, personal, ventas y finanzas.

[![Vue 3](https://img.shields.io/badge/Vue.js-3-%234FC08D?logo=vuedotjs&logoColor=white&style=flat-square)](https://v3.vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-%23009688?logo=fastapi&logoColor=white&style=flat-square)](https://fastapi.tiangolo.com/)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-%233776AB?logo=python&logoColor=white&style=flat-square)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-%234479A5?logo=mysql&logoColor=white&style=flat-square)](https://www.mysql.com/)

## 🚀 ¿Qué es ControlAS Bar?

Sistema completo diseñado específicamente para bares, discotecas y establecimientos nocturnos. Resuelve los principales dolores operativos: inventario caótico, control de personal, facturación manual, reportes tardíos y falta de trazabilidad.

## ✨ Funcionalidades principales

- **Autenticación segura** → Login moderno + flujo completo de recuperación de contraseña
- **Gestión jerárquica** → Roles: Gestor Principal, Dueños, Administradores
- **Control de personal** → Alertas automáticas de exámenes médicos, asignación y seguimiento de tareas
- **Inventario digital** → Productos, categorías, stock en tiempo real, carga de fichas técnicas (PDF)
- **Finanzas automatizadas** → Facturación diaria, control de gastos, cierres de caja, resúmenes mensuales por email
- **Mantenimiento del sistema** → Backups automáticos nocturnos, limpieza programada de históricos
- **Reportes e insights** → Dashboards claros y envíos automáticos de métricas clave

## 🛠️ Stack Tecnológico

| Capa              | Tecnología                          |
|-------------------|-------------------------------------|
| Frontend          | Vue 3 (Composition API) + Vite      |
| Estilos           | Tailwind CSS                        |
| Backend           | FastAPI (Python 3.12) + Uvicorn     |
| Base de datos     | MySQL 8                             |
| Servidor          | Nginx (proxy reverso)               |
| Sistema operativo | Ubuntu LTS                          |
| Seguridad         | SSL Let's Encrypt + Cloudflare      |
| Alertas / Emails  | SMTP + programador de tareas        |
| CI/CD             | Git pull + build automatizado + Cloudflare cache purge |

## 📁 Estructura del proyecto

ControlAS/
├── bar_backend/          # API REST con FastAPI
│   ├── app/
│   │   ├── models/       # Modelos SQLAlchemy
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── crud/         # Lógica de acceso a datos
│   │   ├── routers/      # Endpoints
│   │   ├── dependencies/
│   │   └── main.py
│   └── requirements.txt
│
├── frond/                # Frontend Vue 3
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── views/
│   │   ├── stores/       # Pinia stores
│   │   ├── router/
│   │   └── main.js
│   ├── public/
│   └── vite.config.js
│
├── scripts/              # Scripts de despliegue, backups, etc.
└── docker/               # (opcional - en roadmap)


## 🔧 Flujo de Despliegue (CI/CD simple pero efectivo)

1. Push al branch `main`
2. Pull en servidor de producción
3. `npm run build` → frontend
4. Reinicio de servicio FastAPI (systemd)
5. Purga de caché Cloudflare → cambios visibles en < 10 segundos

## 📊 Estado actual (Febrero 2026)

- ✅ 6 locales operando en producción  
- ✅ Interfaz 100% responsive y con animaciones suaves  
- ✅ Envío automático de reportes diarios y mensuales  
- ✅ Certificados SSL activos y renovados automáticamente  
- ⚙️ Mejorando: PWA + notificaciones push (roadmap 2026)

## 👤 Autor

**Diego Sánchez**  
Desarrollador full-stack enfocado en soluciones prácticas para la gestión operativa de negocios nocturnos.  
Bogotá, Colombia

## 📬 Contacto / Interesado?

Si quieres conocer una demo, cotizar implementación en tu local o colaborar en el proyecto → escríbeme por LinkedIn o por aquí.

¡Gracias por llegar hasta acá! 🍻

