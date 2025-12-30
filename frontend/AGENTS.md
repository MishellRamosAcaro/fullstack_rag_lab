# AGENTS.md — Frontend

This document defines how agents (AI or automation) must operate within the **frontend** environment of the `full_rag_lab` repository.

---

## 1. Core Technology Stack

- **Framework:** Vue 3 (Composition API)
- **Script Style:** `<script setup>`
- **State Management:** `ref()` preferred over `reactive()`
- **Routing:** Vue Router 4 (Lazy loading for all views)
- **HTTP Client:** Axios (Centralized instance)
- **Styling:** Tailwind CSS (Utility-first approach, avoid custom CSS files when possible)
- **Language:** English (Code, Comments, UI Text, and Error Messages)

---

## 2. Architecture & Principles (SOLID, KISS, DRY)

### Separation of Concerns
- Components must focus only on UI and user interaction.
- Business logic, state, and side effects must be extracted into **Composables**:
  - Location: `src/composables/`
  - Naming: `useXxx.js`

### DRY Principle
- All HTTP requests must go through a **centralized Axios instance**:
  - Location: `src/api/axios.js`
- Reusable UI elements must be abstracted into base components:
  - Examples: `BaseButton.vue`, `BaseModal.vue`, `BaseCard.vue`

### KISS Principle
- Components must remain small and readable.
- If a component exceeds **300 lines**, it must be split into smaller components or composables.

### Naming Conventions
- **Components:** PascalCase + semantic suffix  
  - Example: `SearchInput.vue`, `ChatView.vue`
- **Composables:** `useXxx.js`  
  - Example: `useSearch.js`, `useRagQuery.js`
- **API files:** descriptive and scoped  
  - Example: `ragApi.js`

---

## 3. Component Standards

### Props & Emits
- Props must always be declared and validated using `defineProps`.
- Emits must always be explicitly declared using `defineEmits`.

### Internal Logic Order
Components must follow this order inside `<script setup>`:

1. Imports
2. Props / Emits definitions
3. Refs / reactive state
4. Computed properties
5. Methods / functions
6. Lifecycle hooks (`onMounted`, `onUnmounted`, etc.)

---

## 4. Security & Performance

### Error Handling
- All API calls must be wrapped in `try / catch / finally`.
- Errors must be:
  - Logged (for debugging)
  - Exposed to the UI in a user-friendly way

### XSS Prevention
- Avoid `v-html` entirely unless explicitly justified.
- Prefer interpolation `{{ }}` or `v-text`.

### Resource Management
- Always clean up:
  - Event listeners
  - Intervals / timeouts
- Use native browser features when possible:
  - `loading="lazy"` for images

---

## 5. API Pattern

- All HTTP communication must go through the centralized Axios service.
- API-specific logic must live in `src/api/`, never inside components.
- No direct `axios` imports inside Vue components.

---

## 6. UI & Component Libraries

- Import **only the components that are strictly necessary**.
- Avoid global component registration unless justified.
- Bundle size and tree-shaking must be considered in all UI decisions.

---

## 7. Code Formatting & Clean Code Rules

- **Indentation:** 2 spaces
- **Quotes:**
  - JavaScript: single quotes `'`
  - HTML attributes: double quotes `"`
- **Semicolons:** Do not use semicolons unless strictly required
- **Function Naming:** Must start with a verb  
  - Examples: `fetchResults`, `handleSubmit`, `resetState`
- **Boolean Naming:** Use `is`, `has`, or `should` prefixes  
  - Examples: `isLoading`, `hasError`, `shouldFetch`

---

## 8. Acceptance Criteria for Frontend Changes

A frontend change is considered complete when:

- The application builds without errors.
- No linting or formatting rules are violated.
- Existing UI behavior is preserved unless explicitly requested.
- New logic is covered by tests when applicable.
- Code follows all conventions defined in this document.

---

## Scope Limitation

- This document applies **only** to the `frontend` environment.
- Backend and database rules are defined in separate `AGENTS.md` files.
