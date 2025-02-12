{/* # /frontend/src/services/api.js */}
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para tratamento de erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    let errorMessage = 'Ocorreu um erro na requisição';

    if (error.response) {
      // Erro retornado pelo servidor
      errorMessage = error.response.data.detail || error.response.data.message;
    } else if (error.request) {
      // Erro de conexão
      errorMessage = 'Não foi possível conectar ao servidor';
    }

    return Promise.reject(new Error(errorMessage));
  }
);

// Funções de API
export const uploadCSV = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/upload-csv', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const exportCSV = async () => {
  return api.get('/export-csv', {
    responseType: 'blob',
  });
};

export const trainModel = async () => {
  return api.post('/train');
};

export const getMetrics = async () => {
  return api.get('/metrics');
};

export const predict = async (records) => {
  return api.post('/predict', { records });
};