# Feature: Secure Login (PrimeVue + Vue 3 Composition API)

## Summary
Implement a secure login experience for the lab console using PrimeVue components and Vue 3 Composition API. Introduce a backend authentication service with PostgreSQL persistence and SQLAlchemy models, along with a service layer for API calls and token handling.

## Context
The application currently exposes the laboratory console without authentication. We need a clean, SOLID-aligned authentication flow with clear UX states (validation, loading, error) and a backend login service that validates users against a PostgreSQL database.

## Requirements
- **Frontend**
  - Use **PrimeVue** components (`Card`, `InputText`, `Password`, `Button`, `Message`).
  - Use **Vue 3 Composition API** (`setup`, `ref`, `computed`) with client-side validation.
  - Provide **loading** and **error** states on login.
  - Add an **auth service layer** for API calls and secure token handling (in-memory + session storage).
  - Add a **route/page** for login and protect the existing console route.
- **Backend**
  - Create `backend/login_services` for authentication logic.
  - Add a **PostgreSQL** service in Docker Compose (latest image).
  - Use **SQLAlchemy** to create and manage the authentication table (`users`) in the database.
  - Implement a `/auth/login` endpoint that validates credentials and returns a JWT access token.
  - Add backend tests covering login success and failure.

## Acceptance Criteria
- Login page is reachable at `/login` and uses PrimeVue components.
- Client-side validation prevents empty/short inputs and shows inline feedback.
- Login button shows loading state; errors are visible on failure.
- Authenticated users can access `/`; unauthenticated users are redirected to `/login`.
- Backend creates a `users` table and supports credential validation.
- `/auth/login` returns a JWT token on success and `401` on invalid credentials.
- Docker Compose includes a running PostgreSQL service named `db`.
- Backend tests validate login success and rejection.

## Proposed Tasks
1. **Routing**
   - Add Vue Router and a dedicated login view.
   - Protect the existing console view behind auth guard.
2. **Login UI**
   - Build PrimeVue login form with validation, loading, and error states.
3. **Auth Service Layer**
   - Create an API service module for login.
   - Implement token storage (in-memory + sessionStorage).
4. **Backend Auth**
   - Add SQLAlchemy models and DB session utilities.
   - Implement `login_services` with password hashing + JWT generation.
   - Expose `/auth/login` route.
5. **Testing**
   - Add backend tests for login success/failure.

## Security Notes
- Store only password hashes in the database (bcrypt).
- Avoid persisting access tokens in long-term storage when possible.
- Keep JWT secrets in environment variables and rotate in production.
- Add rate-limiting and audit logging in future iterations.
