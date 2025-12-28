import axios from "axios";
import { getAuthToken } from "./authToken";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

apiClient.interceptors.request.use((config) => {
  const token = getAuthToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const uploadDocuments = async (files, onUploadProgress) => {
  const formData = new FormData();
  files.forEach((file) => formData.append("files", file));
  const { data } = await apiClient.post("/rag/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
    onUploadProgress,
  });
  return data;
};

export const processDocuments = async () => {
  const { data } = await apiClient.post("/rag/process");
  return data;
};

export const resetDocuments = async () => {
  const { data } = await apiClient.delete("/rag/reset");
  return data;
};

export const queryRag = async (question) => {
  const { data } = await apiClient.post("/rag/query", { question });
  return data;
};

export const resetRag = async () => {
  const { data } = await apiClient.post("/rag/reset");
  return data;
};

export default apiClient;
