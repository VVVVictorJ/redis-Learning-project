import axios from 'axios';

const http = axios.create({
  baseURL: '/api/v1', // Set base URL to include API version
  timeout: 10000, // Request timeout
});

// Request interceptor
http.interceptors.request.use(
  config => {
    // Here you can add logic like adding an auth token to headers
    // const token = localStorage.getItem('token');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// Response interceptor
http.interceptors.response.use(
  response => response,
  error => {
    // Handle global errors here
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export default http; 