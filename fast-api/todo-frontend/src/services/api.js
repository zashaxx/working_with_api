import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  register: async (userData) => {
    const response = await api.post("/auth/", userData);
    return response.data;
  },

  login: async (username, password) => {
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    const response = await api.post("/auth/token", formData, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });
    return response.data;
  },
};

// Todo API
export const todoAPI = {
  getAllTodos: async () => {
    const response = await api.get("/todos/");
    return response.data;
  },

  getTodoById: async (id) => {
    const response = await api.get(`/todos/todo/${id}`);
    return response.data;
  },

  createTodo: async (todoData) => {
    const response = await api.post("/todos/todo/add-todo", todoData);
    return response.data;
  },

  updateTodo: async (id, todoData) => {
    const response = await api.put(`/todos/todo/${id}`, todoData);
    return response.data;
  },

  deleteTodo: async (id) => {
    const response = await api.delete(`/todos/todo/${id}`);
    return response.data;
  },
};

export default api;
