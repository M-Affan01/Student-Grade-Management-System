/**
 * API Service Module
 * ===================
 * Axios-based HTTP client for communicating with the Flask backend.
 * Provides typed service objects for student CRUD operations and
 * storage management.
 *
 * All requests include a 60-second timeout and automatic error
 * interception for connection and timeout issues.
 *
 * @module api
 */

import axios from "axios";

/** Base URL for all API requests */
const API_BASE = "http://localhost:5002/api";

/**
 * Axios instance configured with base URL, headers, and timeout.
 * @type {import('axios').AxiosInstance}
 */
const api = axios.create({
  baseURL: API_BASE,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 60000,
});

/**
 * Response interceptor for global error handling.
 * Converts timeout errors to user-friendly messages and detects
 * network connectivity issues.
 */
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === "ECONNABORTED") {
      error.message = "Request timed out. Please try again.";
    } else if (!error.response) {
      error.message = "Cannot connect to server. Is the backend running?";
    }
    return Promise.reject(error);
  }
);

/**
 * Student API Service
 * ====================
 * Provides methods for all student CRUD operations and queries.
 *
 * @namespace studentService
 */
export const studentService = {
  /**
   * Get all students.
   * @returns {Promise<AxiosResponse>} Response with array of student objects.
   */
  getAll: () => api.get("/students"),

  /**
   * Get a single student by their unique ID.
   * @param {number} id - The student's unique identifier.
   * @returns {Promise<AxiosResponse>} Response with student object.
   */
  getById: (id) => api.get(`/students/${id}`),

  /**
   * Get a student by their list index (0-based).
   * @param {number} index - Zero-based position in the list.
   * @returns {Promise<AxiosResponse>} Response with student object.
   */
  getByIndex: (index) => api.get(`/students/index/${index}`),

  /**
   * Create a new student.
   * @param {Object} data - Student data.
   * @param {string} data.name - Student's full name (required, 2-100 chars).
   * @param {number} data.grade - Student's grade (required, 0-100).
   * @param {string} data.email - Student's email (required, valid provider).
   * @param {string} data.subject - Student's subject (required, 2-100 chars).
   * @returns {Promise<AxiosResponse>} Response with created student object.
   */
  create: (data) => api.post("/students", data),

  /**
   * Update an existing student by ID.
   * @param {number} id - The student's unique identifier.
   * @param {Object} data - Updated student data (any subset of fields).
   * @returns {Promise<AxiosResponse>} Response with updated student object.
   */
  update: (id, data) => api.put(`/students/${id}`, data),

  /**
   * Update only the grade of a student at a given index.
   * @param {number} index - Zero-based position of the student.
   * @param {number} grade - New grade value (0-100).
   * @returns {Promise<AxiosResponse>} Response with updated student object.
   */
  updateGrade: (index, grade) => api.put(`/students/index/${index}/grade`, { grade }),

  /**
   * Delete a student by their unique ID.
   * @param {number} id - The student's unique identifier.
   * @returns {Promise<AxiosResponse>} Response with deletion confirmation.
   */
  delete: (id) => api.delete(`/students/${id}`),

  /**
   * Delete a student by their list index.
   * @param {number} index - Zero-based position of the student.
   * @returns {Promise<AxiosResponse>} Response with deletion confirmation.
   */
  deleteByIndex: (index) => api.delete(`/students/index/${index}`),

  /**
   * Search students by name (case-insensitive partial match).
   * @param {string} name - Search query string.
   * @returns {Promise<AxiosResponse>} Response with search results.
   */
  search: (name) => api.get("/students/search", { params: { name } }),

  /**
   * Get all students sorted by grade.
   * @param {boolean} ascending - Sort direction. True = ascending, false = descending.
   * @returns {Promise<AxiosResponse>} Response with sorted student array.
   */
  sortByGrade: (ascending = true) => api.get(`/students/sort`, { params: { ascending } }),

  /**
   * Get class statistics (average, highest, lowest, pass/fail counts, grade distribution).
   * @returns {Promise<AxiosResponse>} Response with statistics object.
   */
  getStats: () => api.get("/students/stats"),

  /**
   * Get the total number of students.
   * @returns {Promise<AxiosResponse>} Response with { size: number }.
   */
  getSize: () => api.get("/students/size"),

  /**
   * Get the average grade across all students.
   * @returns {Promise<AxiosResponse>} Response with { average: number }.
   */
  getAverage: () => api.get("/students/average"),

  /**
   * Get the highest grade among all students.
   * @returns {Promise<AxiosResponse>} Response with { highest: number }.
   */
  getHighest: () => api.get("/students/highest"),

  /**
   * Get the lowest grade among all students.
   * @returns {Promise<AxiosResponse>} Response with { lowest: number }.
   */
  getLowest: () => api.get("/students/lowest"),
};

/**
 * Storage API Service
 * ====================
 * Provides methods for storage backend management (save/load/info).
 *
 * @namespace storageService
 */
export const storageService = {
  /**
   * Get information about the active storage backend.
   * @returns {Promise<AxiosResponse>} Response with storage type, count, and details.
   */
  getInfo: () => api.get("/storage/info"),

  /**
   * Manually save data to the storage backend.
   * @returns {Promise<AxiosResponse>} Response with save confirmation message.
   */
  save: () => api.post("/storage/save"),

  /**
   * Manually reload data from the storage backend.
   * @returns {Promise<AxiosResponse>} Response with load confirmation and count.
   */
  load: () => api.post("/storage/load"),
};

export default api;
