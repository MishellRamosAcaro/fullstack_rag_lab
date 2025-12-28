import apiClient from "./api";
import { setAuthToken } from "./authToken";

export const login = async ({ identifier, password }) => {
  const { data } = await apiClient.post("/auth/login", { identifier, password });
  setAuthToken(data.access_token);
  return data;
};
