# Lab RAG POC

Fullstack proof of concept for a laboratory knowledge console. FastAPI + LangChain + OpenAI (Chroma in-memory) on the backend and Vue 3 + PrimeVue on the frontend let you upload lab documents, process them, and chat with answers that cite sources.

## Features / Características
- Carga de PDF, Markdown, DOCX y TXT (máx. 10 MB por archivo, 10 archivos en memoria).
- Paso manual de procesado con barra de progreso; embeddings y vector store viven en memoria para la sesión.
- Chat con historial, respuesta contextual y listado de fuentes (archivo + página).
- Botón de reset para limpiar archivos, chunks y estado de chat.

## Backend
- Stack: FastAPI, LangChain, OpenAI, Chroma (en memoria para el POC).
- Endpoints principales:
  - `POST /rag/upload` form-data `files[]` -> `{ uploaded, rejected, total_files }`
  - `POST /rag/process` -> `{ status, chunks }`
  - `POST /rag/query` `{ question }` -> `{ answer, chunks }`
  - `DELETE /rag/reset` -> `{ status, files_cleared, chunks_cleared }`
- Validaciones: 10 archivos máximo, 10 MB cada uno, extensiones permitidas `.pdf .md .markdown .txt .docx`, pregunta no vacía.
- Variables de entorno (colocarlas en `.env` o exportarlas):
  ```
  OPENAI_API_KEY=tu_api_key
  OPENAI_MODEL=gpt-4o-mini            # opcional, por defecto
  EMBEDDING_MODEL=text-embedding-3-small
  CHUNK_SIZE=800
  CHUNK_OVERLAP=100
  K_RESULTS=5
  TEMPERATURE=0.1
  ```
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
- Flujo UI: subir archivos -> “Process” -> preguntar en el chat -> revisar fuentes -> “Reset” para limpiar sesión.
- Config: crear `.env` en `frontend/` con `VITE_API_BASE_URL=http://localhost:8000` (o la URL del backend).
- Ejecutar local:
  ```bash
  cd frontend
  npm install
  npm run dev -- --host --port 5173
  ```

## Docker / Compose
- Imágenes:
  - Backend: `backend/Dockerfile`
  - Frontend estático: `frontend/Dockerfile`
- Levantar todo desde la raíz:
  ```bash
  docker-compose up --build
  ```
  - Backend en `http://localhost:8000`
  - Frontend en `http://localhost:5173`

## Límites y notas
- 10 archivos máx. cargados a la vez, 10 MB c/u.
- Documentos y vector store están en memoria; al reiniciar el backend se pierden.
- Respuestas incluyen sección de “Sources” con archivo y página para trazabilidad.
