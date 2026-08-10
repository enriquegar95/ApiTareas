# API Tareas

🔗 **Desplegado en:** [api-tareas-chi.vercel.app](https://api-tareas-chi.vercel.app)

API REST para la gestión de tareas, desarrollada con **Python, FastAPI, SQLAlchemy y PostgreSQL**. El proyecto está dockerizado y utiliza **Alembic** para la gestión de migraciones de base de datos.

## Tecnologías

* **Python 3.12**
* **FastAPI** — framework para la API REST
* **Pydantic** — validación y serialización de datos
* **SQLAlchemy 2.x** — ORM
* **PostgreSQL 16** — base de datos
* **Alembic** — migraciones
* **Docker / Docker Compose** — contenedores
* **pgAdmin** — administración de PostgreSQL
* **Swagger / OpenAPI** — documentación interactiva

## Arquitectura

El proyecto está organizado por responsabilidades:

```text
api-tareas/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   └── tareas.py
│   │       └── router.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   ├── base.py
│   │   └── seed.py
│   │
│   ├── models/
│   │   ├── tarea.py
│   │   ├── prioridad.py
│   │   └── estado.py
│   │
│   ├── schemas/
│   │   └── tarea.py
│   │
│   └── main.py
│
├── alembic/
│   └── versions/
│
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── requirements.txt
└── README.md
```

## Modelo de datos

La aplicación utiliza tres entidades principales:

### Tarea

Una tarea contiene:

* `id`
* `titulo`
* `descripcion`
* `fecha_creacion`
* `fecha_modificacion`
* `prioridad_id`
* `estado_id`

### Prioridad

Catálogo de prioridades disponibles:

* Baja
* Media
* Alta
* Urgente

### Estado

Catálogo de estados disponibles:

* Pendiente
* En Progreso
* En Pausa
* Completada

Las relaciones son:

```text
Prioridad 1 ──────── N Tarea N ──────── 1 Estado
```

Cada tarea tiene una prioridad y un estado.

## Validación

Los datos recibidos por la API se validan mediante esquemas Pydantic.

Por ejemplo, el título de una tarea:

```python
titulo: str = Field(
    ...,
    min_length=1,
    max_length=100
)
```

De esta forma, la API rechaza automáticamente valores que no cumplan las restricciones definidas.

## Base de datos

SQLAlchemy se utiliza como ORM para trabajar con PostgreSQL mediante modelos Python.

La configuración de la conexión y la sesión se define en `app/db/database.py`, donde también se declara la clase `Base` de la que heredan los modelos. El módulo `app/db/base.py` importa los modelos para que Alembic detecte el metadata completo al autogenerar migraciones.

Los modelos heredan de `Base`:

```python
class Tarea(Base):
    __tablename__ = "tareas"
```

Las relaciones entre tablas se gestionan mediante `ForeignKey` y `relationship`.

## Migraciones

Las modificaciones del esquema de base de datos se gestionan con **Alembic**.

Crear una nueva migración:

```bash
docker compose exec api alembic revision --autogenerate -m "descripcion"
```

Aplicar las migraciones:

```bash
docker compose exec api alembic upgrade head
```

Consultar la versión actual:

```bash
docker compose exec api alembic current
```

## Datos iniciales

Al iniciar la aplicación se ejecuta un proceso de seed que comprueba si existen los catálogos básicos.

Si no existen, se crean:

```text
Prioridades:
- Baja
- Media
- Alta
- Urgente

Estados:
- Pendiente
- En Progreso
- En Pausa
- Completada
```

El proceso es idempotente: si los registros ya existen, no se vuelven a insertar.

## Docker

El proyecto utiliza Docker Compose para ejecutar los diferentes servicios.

Levantar el proyecto:

```bash
docker compose up -d
```

Comprobar los contenedores:

```bash
docker compose ps
```

Ver los logs de la API:

```bash
docker compose logs -f api
```

Detener los servicios:

```bash
docker compose down
```

## Documentación de la API

Con los contenedores levantados, FastAPI genera automáticamente la documentación OpenAPI.

### Swagger UI

```text
http://localhost:8000/docs
```

### OpenAPI

```text
http://localhost:8000/openapi.json
```

Swagger permite probar los endpoints directamente desde el navegador.

## Estructura de la aplicación

El flujo principal de una petición es:

```text
Cliente
   │
   ▼
FastAPI
   │
   ▼
Router
   │
   ▼
Endpoint
   │
   ├── Pydantic → validación
   │
   ├── Depends → obtiene sesión DB
   │
   ▼
SQLAlchemy
   │
   ▼
PostgreSQL
```

La respuesta realiza el camino inverso:

```text
PostgreSQL
   │
   ▼
SQLAlchemy ORM
   │
   ▼
Pydantic Schema
   │
   ▼
FastAPI
   │
   ▼
JSON
```

## Estado del proyecto

**Backend funcional.** La API cuenta con operaciones CRUD de tareas, conexión con PostgreSQL, modelos SQLAlchemy con relaciones entre entidades, validación con Pydantic, migraciones con Alembic, seed idempotente de datos iniciales, Docker Compose y documentación automática con Swagger.

El objetivo del proyecto fue practicar el desarrollo backend con Python y FastAPI, por lo que el foco está en la API; el frontend es mínimo. Actualmente el proyecto está en pausa, ya que he orientado mi formación hacia el desarrollo backend con Java y Spring Boot.

Los endpoints CRUD de tareas se implementan en:

```text
app/api/v1/endpoints/tareas.py
```

## Objetivos del proyecto

Este proyecto tiene como objetivo practicar y consolidar conceptos de desarrollo backend con Python:

* Diseño de APIs REST
* FastAPI
* Programación orientada a objetos
* SQLAlchemy ORM
* Relaciones entre entidades
* PostgreSQL
* Pydantic
* Inyección de dependencias
* Migraciones con Alembic
* Docker y Docker Compose
* Documentación OpenAPI
* Arquitectura organizada por capas