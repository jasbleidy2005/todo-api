# ToDo API - Sistema de Gestión de Tareas

API REST para gestionar tareas (to-do list) asociadas a usuarios, desarrollada con Flask y PostgreSQL.

## Estructura del Proyecto

```
API-ToDo/
├── src/
│   ├── models/           # Modelos de datos (User, Task)
│   ├── services/         # Lógica de negocio (UserService, TaskService)
│   ├── controllers/      # Controladores HTTP (UserController, TaskController)
│   ├── routes/           # Definición de endpoints
│   └── config/           # Configuración de BD y aplicación
├── tests/
│   ├── unit/             # Pruebas unitarias
│   ├── integration/      # Pruebas de integración
│   └── e2e/              # Pruebas end-to-end
├── .github/
│   └── workflows/        # CI/CD con GitHub Actions
├── app.py                # Punto de entrada de la aplicación
├── requirements.txt      # Dependencias de Python
├── .env.example          # Plantilla de variables de entorno
├── .bandit               # Configuración de análisis estático
└── README.md             # Este archivo
```

## Tecnologías Utilizadas

- **Lenguaje:** Python 3.11+
- **Framework:** Flask 3.0
- **ORM:** SQLAlchemy
- **Base de Datos:** PostgreSQL 17
- **Testing:** pytest, pytest-flask
- **Análisis Estático:** Bandit
- **CI/CD:** GitHub Actions

## Modelo de Datos

### Tabla User
- `id` (PK, Integer, Autoincremental)
- `name` (String, Requerido)
- `email` (String, Requerido, Único)
- `created_at` (Timestamp)

### Tabla Task
- `id` (PK, Integer, Autoincremental)
- `title` (String, Requerido)
- `description` (Text, Opcional)
- `is_completed` (Boolean, Default: False)
- `user_id` (FK → User.id)
- `created_at` (Timestamp)

## Endpoints Disponibles

### Usuarios

#### POST /api/users - Crear usuario
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"Juan Pérez\", \"email\": \"juan@example.com\"}"
```

**Respuesta exitosa (201):**
```json
{
  "message": "Usuario creado exitosamente",
  "user": {
    "id": 1,
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "created_at": "2025-11-21T10:30:00"
  }
}
```

#### GET /api/users/:id - Consultar usuario por ID
```bash
curl -X GET http://localhost:5000/api/users/1
```

**Respuesta exitosa (200):**
```json
{
  "user": {
    "id": 1,
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "created_at": "2025-11-21T10:30:00"
  }
}
```

### Tareas

#### POST /api/tasks - Crear tarea
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Comprar leche\", \"description\": \"Ir al supermercado\", \"user_id\": 1}"
```

**Respuesta exitosa (201):**
```json
{
  "message": "Tarea creada exitosamente",
  "task": {
    "id": 1,
    "title": "Comprar leche",
    "description": "Ir al supermercado",
    "is_completed": false,
    "user_id": 1,
    "created_at": "2025-11-21T10:35:00"
  }
}
```

#### GET /api/users/:id/tasks - Listar tareas de un usuario
```bash
curl -X GET http://localhost:5000/api/users/1/tasks
```

**Respuesta exitosa (200):**
```json
{
  "user_id": 1,
  "tasks": [
    {
      "id": 1,
      "title": "Comprar leche",
      "description": "Ir al supermercado",
      "is_completed": false,
      "user_id": 1,
      "created_at": "2025-11-21T10:35:00"
    }
  ],
  "total": 1
}
```

#### PUT /api/tasks/:id - Actualizar estado de tarea
```bash
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d "{\"is_completed\": true}"
```

**Respuesta exitosa (200):**
```json
{
  "message": "Tarea actualizada exitosamente",
  "task": {
    "id": 1,
    "title": "Comprar leche",
    "is_completed": true,
    "user_id": 1
  }
}
```

#### PATCH /api/tasks/:id/complete - Marcar tarea como completada
```bash
curl -X PATCH http://localhost:5000/api/tasks/1/complete
```

**Respuesta exitosa (200):**
```json
{
  "message": "Tarea marcada como completada",
  "task": {
    "id": 1,
    "title": "Comprar leche",
    "is_completed": true,
    "user_id": 1
  }
}
```

#### DELETE /api/tasks/:id - Eliminar tarea
```bash
curl -X DELETE http://localhost:5000/api/tasks/1
```

**Respuesta exitosa (200):**
```json
{
  "message": "Tarea con ID 1 eliminada exitosamente"
}
```

## Instalación y Configuración

### Requisitos Previos
- Python 3.11 o superior
- PostgreSQL 17
- pip (gestor de paquetes de Python)

### Paso 1: Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd API-ToDo
```

### Paso 2: Crear entorno virtual
```bash
python -m venv venv
```

### Activar entorno virtual:
**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Paso 3: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Configurar base de datos PostgreSQL

#### Opción A: Crear base de datos manualmente
```sql
-- Conectarse a PostgreSQL
psql -U postgres

-- Crear la base de datos
CREATE DATABASE tasks_management_db;

-- Verificar creación
\l
```

#### Opción B: Script SQL
Crear un archivo `setup_db.sql` con:
```sql
CREATE DATABASE IF NOT EXISTS tasks_management_db;
```

Ejecutar:
```bash
psql -U postgres -f setup_db.sql
```

### Paso 5: Configurar variables de entorno
Copiar `.env.example` a `.env`:
```bash
copy .env.example .env
```

Editar `.env` con tus credenciales:
```env
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=tasks_management_db
DATABASE_USER=postgres
DATABASE_PASSWORD=admin123
FLASK_ENV=development
FLASK_DEBUG=True
```

### Paso 6: Inicializar la base de datos
Las tablas se crean automáticamente al iniciar la aplicación por primera vez.

### Paso 7: Ejecutar la aplicación
```bash
python app.py
```

La API estará disponible en: `http://localhost:5000`

## Ejecutar Pruebas

### Pruebas Unitarias (4 pruebas)
```bash
pytest tests/unit/ -v
```

Validan:
- No se puede crear usuario con email duplicado
- No se puede crear tarea sin user_id
- is_completed se actualiza correctamente
- Se puede eliminar una tarea

### Pruebas de Integración (3 pruebas)
```bash
pytest tests/integration/ -v
```

Validan:
- POST /api/users retorna código 201
- POST /api/tasks verifica asociación con usuario
- GET /api/users/:id/tasks lista tareas correctamente

### Prueba End-to-End (1 flujo completo)
```bash
pytest tests/e2e/ -v
```

Flujo validado:
1. Crear usuario
2. Crear 2 tareas para ese usuario
3. Listar tareas del usuario
4. Marcar una tarea como completada
5. Eliminar una tarea
6. Verificar que solo queda 1 tarea

### Ejecutar todas las pruebas
```bash
pytest tests/ -v
```

## Análisis Estático de Seguridad

Ejecutar Bandit para detectar vulnerabilidades:
```bash
bandit -r src/ -c .bandit
```

## Validaciones de Negocio Implementadas

1. **Email único:** No se permite crear usuarios con email duplicado
2. **Validar user_id:** No se puede crear tarea sin user_id válido
3. **Usuario existente:** Se verifica que el user_id exista antes de crear tarea
4. **Actualización controlada:** Solo se permite actualizar el campo is_completed

## Códigos de Estado HTTP

- `200 OK` - Operación exitosa (GET, PUT, DELETE)
- `201 Created` - Recurso creado exitosamente (POST)
- `400 Bad Request` - Datos inválidos o validación de negocio fallida
- `404 Not Found` - Recurso no encontrado
- `500 Internal Server Error` - Error interno del servidor

## CI/CD con GitHub Actions

El pipeline se ejecuta automáticamente en cada push o pull request a las ramas `main` y `develop`.

**Flujo del pipeline:**
1. Instalar dependencias
2. Ejecutar pruebas unitarias
3. Ejecutar pruebas de integración
4. Ejecutar prueba E2E
5. Ejecutar análisis estático con Bandit
6. Si TODO pasa → Imprimir "OK"
7. Si ALGO falla → Marcar como Failed

Ver estado del pipeline en la pestaña "Actions" de GitHub.

## Arquitectura por Capas

### Capa de Modelos (models/)
Define la estructura de datos y relaciones con la base de datos usando SQLAlchemy ORM.

### Capa de Servicios (services/)
Contiene la lógica de negocio. Las validaciones y reglas de negocio se implementan aquí.

### Capa de Controladores (controllers/)
Maneja las peticiones HTTP, valida datos de entrada y formatea respuestas JSON.

### Capa de Rutas (routes/)
Define los endpoints de la API y los asocia con los controladores correspondientes.

### Capa de Configuración (config/)
Gestiona la configuración de la aplicación y la conexión a la base de datos.

## Posibles Problemas y Soluciones

### Error: "Relation does not exist"
**Solución:** Verificar que las tablas se crearon correctamente. Reiniciar la aplicación.

### Error: "FATAL: password authentication failed"
**Solución:** Verificar credenciales en el archivo `.env`.

### Error: "Port 5000 already in use"
**Solución:** Cambiar el puerto en `app.py` o cerrar la aplicación que está usando el puerto 5000.

### Error al importar módulos en pruebas
**Solución:** Verificar que el entorno virtual esté activado y que todas las dependencias estén instaladas.

## Tiempo Estimado de Desarrollo

- Estructura y configuración: 15 minutos
- Modelos: 10 minutos
- Servicios: 20 minutos
- Controladores y rutas: 20 minutos
- Pruebas unitarias: 15 minutos
- Pruebas de integración: 10 minutos
- Prueba E2E: 10 minutos
- GitHub Actions: 10 minutos
- Documentación: 10 minutos

**Total estimado:** 2 horas (margen de 20 minutos sobre el tiempo del parcial)

## Licencia

Este proyecto es para fines educativos.
