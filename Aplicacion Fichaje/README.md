# 🏢 Sistema de Fichaje de Oficina

Aplicación web en Python/Flask para controlar entradas y salidas de empleados.

## Requisitos

- Python 3.8+
- Flask (`pip install flask`)

## Arrancar la aplicación

```bash
cd fichaje
python app.py
```

Luego abre **http://127.0.0.1:5000** en tu navegador.

## Funciones

| Pantalla | Qué hace |
|---|---|
| **Fichar** | Cards de empleados → selecciona tu nombre → introduce PIN → registra entrada o salida automáticamente |
| **Historial** | Lista de todos los fichajes con buscador en tiempo real |
| **Empleados** | Alta de nuevos empleados, activar/desactivar existentes |

## Empleados de ejemplo (PIN)

| Nombre | PIN |
|---|---|
| Ana García | 1234 |
| Carlos Martínez | 5678 |
| Laura Sánchez | 9012 |

## Estructura

```
fichaje/
├── app.py              # Lógica Flask + SQLite
├── fichaje.db          # Base de datos (se crea automáticamente)
├── README.md
└── templates/
    ├── base.html       # Layout y estilos comunes
    ├── index.html      # Pantalla de fichaje con teclado PIN
    ├── historial.html  # Historial de registros
    └── empleados.html  # Gestión de empleados
```

## API JSON

`GET /api/estado` → devuelve JSON con el estado actual de todos los empleados.
