# 🤖 Guía de Agentes y Estándares de Desarrollo (Backend)

Este documento define las directrices obligatorias para el desarrollo en el **backend**. Todos los agentes (IA) y colaboradores deben seguir estas reglas para garantizar la calidad y seguridad del código ejecutado en contenedores.

---

## 🏗️ Arquitectura y Diseño

* **Principios SOLID:** Cada clase debe tener una única responsabilidad.
* **KISS (Keep It Simple, Stupid):** Prioriza la simplicidad y legibilidad.
* **DRY (Don't Repeat Yourself):** Abstrae lógica común para evitar duplicidad.
* **Arquitectura de Capas:** Mantén una separación clara entre la lógica de negocio, el acceso a datos y la interfaz de entrada.

---

## 🐍 Entorno de Desarrollo (Python 3.13.7)

El código se desarrolla localmente pero se ejecuta dentro de un contenedor Docker mediante volúmenes compartidos.

* **Versión:** Python 3.13.7. Utiliza características modernas (f-strings avanzadas, mejoras en tipos, etc.).
* **Gestión de Dependencias:** Cualquier nueva librería debe añadirse al `requirements.txt` para que el contenedor la reconozca.
* **Paths Dinámicos:** No uses rutas absolutas de tu máquina local. Usa la librería `pathlib` y asume que la raíz es el directorio de trabajo dentro del Docker.
* **Tipado Estricto:** Es obligatorio el uso de *Type Hints* en todas las funciones.

---

## 🐳 Docker & Ejecución

* **Volúmenes:** Ten en cuenta que los cambios en el código se reflejan en tiempo real en el contenedor. No generes archivos temporales pesados en el volumen compartido que puedan ralentizar el sistema de archivos (usa `/tmp` dentro del contenedor si es necesario).
* **Variables de Entorno:** El agente debe buscar la configuración en variables de entorno o en `.env` dentro de `backend/`.
* **Logs de Salida:** Asegúrate de que los logs se envíen a `stdout/stderr` para que sean visibles mediante `docker logs`.

---

## 🛡️ Seguridad y Estilo

* **Secretos:** Nunca escribas credenciales en el código. Usa archivos `.env` (asegurándote de que estén en `.gitignore`).
* **Seguridad en Docker:** No asumas que el contenedor corre como `root`. Escribe código que no dependa de permisos de superusuario a menos que sea estrictamente necesario.
* **PEP 8 & Calidad:** El código debe ser formateado con `black` y validado con `mypy`.
* **Manejo de Excepciones:** Captura errores específicos. Evita que un error no controlado detenga el proceso del contenedor.

---

## 🧪 Pruebas y Calidad

* **Pytest:** Toda funcionalidad nueva debe incluir tests unitarios que puedan ejecutarse dentro del contenedor.
* **Mocking:** Realiza mocks de servicios externos para asegurar que los tests sean rápidos y no dependan de la red del host.

---

## 🧩 Información específica del backend

### 📌 Entrypoint y estructura

* **`backend/main.py`** es el entrypoint de FastAPI y registra los routers:
  * `/rag` (RAG flow).
  * `/auth` (login con JWT).
* **Capas principales**:
  * **Routers:** `backend/routers/*.py`.
  * **Services:** `backend/services/*.py`.
  * **Data layer:** `backend/database.py`, `backend/models.py`.
  * **Schemas:** `backend/schemas.py` (Pydantic).
  * **Config:** `backend/config/settings.py` (Pydantic BaseSettings).

### 🔐 Autenticación

* Login en `POST /auth/login` con `identifier` (username/email) + `password`.
* Servicio: `backend/services/auth_service.py`.
* JWT configurado en `LoginSettings` (`jwt_secret_key`, `jwt_algorithm`, `access_token_expire_minutes`).
* Hashing de contraseñas con **passlib + bcrypt**.

### 🧠 Flujo RAG

* Router: `backend/routers/rag.py`.
* Servicio: `backend/services/rag_service.py`.
* **Flujo**:
  1. Upload de documentos en memoria (`/rag/upload`).
  2. Procesado en chunks (`/rag/process`).
  3. Consulta (`/rag/query`).
  4. Reset en memoria (`/rag/reset`).
* **Tipos soportados**: `.pdf`, `.docx`, `.md`, `.markdown`, `.txt`.
* **Límites actuales**:
  * Máx. **10 archivos** por sesión.
  * Máx. **10MB** por archivo.

### 🗄️ Base de datos

* ORM: **SQLAlchemy**.
* Declarative Base en `backend/database.py`.
* Modelos en `backend/models.py`.
* Dependencia `get_db` para inyección de sesión.

### ⚙️ Configuración (env vars clave)

Las variables se leen desde `.env` o entorno mediante Pydantic Settings.

* **RAGSettings** (`backend/config/settings.py`):
  * `OPENAI_API_KEY`
  * `OPENAI_MODEL`
  * `EMBEDDING_MODEL`
  * `DOCS_PATH`
  * `CHROMA_DIR`
  * `CHUNK_SIZE`
  * `CHUNK_OVERLAP`
  * `K_RESULTS`
  * `TEMPERATURE`
* **LoginSettings**:
  * `JWT_SECRET_KEY`
  * `JWT_ALGORITHM`
  * `ACCESS_TOKEN_EXPIRE_MINUTES`
* **DatabaseSettings**:
  * `DRIVERNAME`, `USERNAME`, `PASSWORD`, `HOST`, `PORT`, `DATABASE`

### 🧪 Tests

* Tests en `backend/tests/`.
* `test_auth.py` cubre login con credenciales válidas e inválidas.
* `conftest.py` inyecta una DB SQLite en memoria para pruebas.

---

> **Instrucción para la IA:** Antes de proponer código, verifica compatibilidad con Python 3.13.7 y usa rutas relativas a la estructura del contenedor.
