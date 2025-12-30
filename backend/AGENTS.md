# 🤖 Agent Guide and Development Standards (Backend)

This document defines the mandatory guidelines for developing the **backend**. All agents (AI) and contributors must follow these rules to ensure quality and security for code executed in containers.

---

## 🏗️ Architecture and Design

* **SOLID Principles:** Each class must have a single responsibility.
* **KISS (Keep It Simple, Stupid):** Prioritize simplicity and readability.
* **DRY (Don't Repeat Yourself):** Abstract common logic to avoid duplication.
* **Layered Architecture:** Maintain a clear separation between business logic, data access, and entry interfaces.

---

## 🐍 Development Environment (Python 3.13.7)

The code is developed locally but runs inside a Docker container via shared volumes.

* **Version:** Python 3.13.7. Use modern features (advanced f-strings, typing improvements, etc.).
* **Dependency Management:** Any new library must be added to `requirements.txt` so the container can install it.
* **Dynamic Paths:** Do not use absolute paths from your local machine. Use `pathlib` and assume the root is the working directory inside Docker.
* **Strict Typing:** Type hints are mandatory for all functions.

---

## 🐳 Docker & Execution

* **Volumes:** Remember code changes are reflected in real time inside the container. Do not generate heavy temporary files in the shared volume that could slow the filesystem (use `/tmp` inside the container if needed).
* **Environment Variables:** The agent must load configuration from environment variables or a `.env` file inside `backend/`.
* **Output Logs:** Ensure logs go to `stdout/stderr` so they are visible via `docker logs`.

---

## 🛡️ Security and Style

* **Secrets:** Never hardcode credentials. Use `.env` files (make sure they are in `.gitignore`).
* **Docker Security:** Do not assume the container runs as `root`. Write code that does not depend on superuser permissions unless strictly required.
* **PEP 8 & Quality:** Code must be formatted with `black` and validated with `mypy`.
* **Exception Handling:** Catch specific errors. Avoid letting unhandled errors crash the container process.

---

## 🧪 Testing and Quality

* **Pytest:** All new functionality must include unit tests that run inside the container.
* **Mocking:** Mock external services to keep tests fast and independent from host networking.

---

## 🧩 Backend-specific information

### 📌 Entrypoint and structure

* **`backend/main.py`** is the FastAPI entrypoint and registers the routers:
  * `/rag` (RAG flow).
  * `/auth` (JWT login).
* **Primary layers**:
  * **Routers:** `backend/routers/*.py`.
  * **Services:** `backend/services/*.py`.
  * **Data layer:** `backend/database.py`, `backend/models.py`.
  * **Schemas:** `backend/schemas.py` (Pydantic).
  * **Config:** `backend/config/settings.py` (Pydantic BaseSettings).

### 🔐 Authentication

* Login at `POST /auth/login` with `identifier` (username/email) + `password`.
* Service: `backend/services/auth_service.py`.
* JWT configured in `LoginSettings` (`jwt_secret_key`, `jwt_algorithm`, `access_token_expire_minutes`).
* Password hashing uses **passlib + bcrypt**.

### 🧠 RAG flow

* Router: `backend/routers/rag.py`.
* Service: `backend/services/rag_service.py`.
* **Flow**:
  1. Upload documents to memory (`/rag/upload`).
  2. Process into chunks (`/rag/process`).
  3. Query (`/rag/query`).
  4. Reset in-memory state (`/rag/reset`).
* **Supported types**: `.pdf`, `.docx`, `.md`, `.markdown`, `.txt`.
* **Current limits**:
  * Max **10 files** per session.
  * Max **10MB** per file.

### 🗄️ Database

* ORM: **SQLAlchemy**.
* Declarative Base in `backend/database.py`.
* Models in `backend/models.py`.
* `get_db` dependency for session injection.

---

> **Instruction for AI:** Before proposing code, verify compatibility with Python 3.13.7 and use paths relative to the container structure.