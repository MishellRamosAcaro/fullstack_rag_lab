# Issue: Login with PrimeVue (Composition API)

## Summary
Add a new login screen using PrimeVue components and Vue 3 Composition API. The implementation should align with clean architecture principles, maintainable UI composition, and secure handling of credentials.

## Context
We need a login flow for the frontend using PrimeVue components. This issue covers UI, state handling, validation, and integration points (API call + secure storage).

## Requirements
- Use **PrimeVue** components for the UI.
- Implement the screen using **Vue 3 Composition API**.
- Follow SOLID/DRY/KISS and clean architecture separation.
- Avoid storing sensitive data in localStorage unless explicitly justified.
- Include clear error handling and loading states.

## Acceptance Criteria
- A dedicated login view is available (route/path as defined in the router).
- UI built with PrimeVue inputs, buttons, and feedback components.
- Composition API hooks (`setup`, `ref`, `computed`) used for state and validation.
- Form validation for email/username + password (client-side).
- Loading state and error messages are visible and accessible.
- API integration is abstracted behind a service layer.
- Unit/Component tests (if applicable in the project) cover validation and error states.

## Proposed Tasks
1. Add login route and page component (Composition API).
2. Create a PrimeVue-based login form UI.
3. Add a service module for authentication API call.
4. Wire up validation + error handling + loading state.
5. Ensure secure token handling per project standards.
6. Add/adjust tests.

## Security Notes
- Use environment variables for API base URL.
- Do not log credentials.
- Prefer HTTP-only cookies if backend supports it.

## References
- PrimeVue documentation
- Vue 3 Composition API guide
