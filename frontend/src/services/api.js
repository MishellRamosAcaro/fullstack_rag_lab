import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ,
});

export const login = async (username, password) => {
  const { data } = await api.post("/rag/login", { username, password });
  return data;
};

export const uploadDocuments = async (files, onUploadProgress) => {
  const formData = new FormData();
  files.forEach((file) => formData.append("files", file));
  const { data } = await api.post("/rag/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
    onUploadProgress,
  });
  return data;
};

export const processDocuments = async () => {
  const { data } = await api.post("/rag/process");
  return data;
};

export const queryRag = async (question) => {
  const { data } = await api.post("/rag/query", { question });
  return data;
};
