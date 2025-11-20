import axios, { AxiosError } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Add session token to requests
api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const sessionId = localStorage.getItem('session_id');
    if (sessionId) {
      config.headers.Authorization = `Bearer ${sessionId}`;
    }
  }
  return config;
});

// Handle errors
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Clear session and redirect to login
      if (typeof window !== 'undefined') {
        localStorage.removeItem('session_id');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/api/auth/login', { email, password }),
  logout: () => api.post('/api/auth/logout'),
  getStatus: () => api.get('/api/auth/status'),
  getCurrentUser: () => api.get('/api/auth/user/me'),
};

// Assignments API
export const assignmentsAPI = {
  list: (params?: {
    course_hash?: string;
    status?: string;
    difficulty?: string;
    limit?: number;
  }) => api.get('/api/assignments', { params }),

  get: (hash: string, courseHash: string) =>
    api.get(`/api/assignments/${hash}`, { params: { course_hash: courseHash } }),

  solve: (hash: string, courseHash: string, mode: 'learning' | 'auto_submit', questions?: string[]) =>
    api.post(`/api/assignments/${hash}/solve`, { mode, questions }, { params: { course_hash: courseHash } }),

  status: (hash: string, courseHash: string) =>
    api.get(`/api/assignments/${hash}/status`, { params: { course_hash: courseHash } }),
};

// Schedule API
export const scheduleAPI = {
  today: () => api.get('/api/schedule/today'),
  week: (startDate?: string) =>
    api.get('/api/schedule/week', { params: { start_date: startDate } }),
  joinClass: (lectureSlotHash: string) =>
    api.post('/api/schedule/join-class', { lecture_slot_hash: lectureSlotHash }),
};

// Performance API
export const performanceAPI = {
  overview: () => api.get('/api/performance/overview'),
  course: (courseHash: string) =>
    api.get(`/api/performance/course/${courseHash}`),
  allCourses: () => api.get('/api/performance/courses'),
};

// Solver API
export const solverAPI = {
  mcq: (question: string, options: Record<string, string>, context?: string) =>
    api.post('/api/solve/mcq', { question, options, context }),

  coding: (problem: string, language: string, testCases?: string, constraints?: string) =>
    api.post('/api/solve/coding', { problem, language, test_cases: testCases, constraints }),

  frontend: (requirements: string, referenceImage?: string) =>
    api.post('/api/solve/frontend', { requirements, reference_image: referenceImage }),
};

export default api;
