const TOKEN_KEY = "lab_auth_token";

let inMemoryToken = null;

export const setAuthToken = (token) => {
  inMemoryToken = token;
  sessionStorage.setItem(TOKEN_KEY, token);
};

export const getAuthToken = () => {
  if (inMemoryToken) return inMemoryToken;
  const stored = sessionStorage.getItem(TOKEN_KEY);
  if (stored) {
    inMemoryToken = stored;
  }
  return stored;
};

export const clearAuthToken = () => {
  inMemoryToken = null;
  sessionStorage.removeItem(TOKEN_KEY);
};
