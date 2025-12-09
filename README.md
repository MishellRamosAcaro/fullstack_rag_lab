# Lab RAG POC

Fullstack proof of concept for a laboratory RAG console. Backend (FastAPI + LangChain + OpenAI + Chroma in-memory) and frontend (Vue 3 + PrimeVue) let you upload lab documents, process them, and chat with traceable sources.

## Features / Características
- Login simulado (credenciales en variables de entorno).
- Carga de PDF, Markdown, DOCX y TXT (máx. 10 MB por archivo, 10 archivos en memoria).
- Procesado manual con barra de progreso; almacenamiento de documentos y embeddings en memoria.
- Chat con historial y sección de fuentes (archivo + página).

## Backend
- Stack: FastAPI, LangChain, OpenAI, Chroma (en memoria para el POC).
- Principales endpoints:
  - `POST /rag/login` `{ username, password }` -> `{ status }`
- `POST /rag/upload` form-data `files[]`
- `POST /rag/process` -> `{ status, chunks }`
- `POST /rag/query` `{ question }` -> `{ answer, chunks }`
- Configuración: variables en `.env` (ver `.env.example` si existiera) con `OPENAI_API_KEY`, modelos, rutas de docs, etc. Para este POC, `CHROMA_DIR` queda en memoria.
- Ejecutar local:
  ```bash
  cd backend
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  uvicorn main:app --reload --host 0.0.0.0 --port 8000
  ```

## Frontend
- Stack: Vite + Vue 3 (Composition API) + PrimeVue + PrimeFlex.
- Config: `VITE_API_BASE_URL` apuntando al backend (por defecto `http://localhost:8000`).
- Ejecutar local:
  ```bash
  cd frontend
  npm install
  npm run dev -- --host --port 5173
  ```
- Flujo UI: login -> subir archivos -> “Process” -> preguntar en el chat (interfaz en inglés, contenido mantiene idioma del documento).

## Docker / Compose
- Imágenes:
  - Backend: `backend/Dockerfile`
  - Frontend estático: `frontend/Dockerfile`
- Levantar todo:
  ```bash
  docker-compose up --build
  ```
  - Backend en `http://localhost:8000`
  - Frontend en `http://localhost:5173`

## Límites y notas
- 10 archivos máx. cargados a la vez, 10 MB c/u.
- Documentos en memoria: si el backend se reinicia, los archivos se pierden.
- Las respuestas incluyen sección “Sources” con archivo y página.
