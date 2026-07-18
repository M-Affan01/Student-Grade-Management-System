import React, { useState, useEffect, useCallback } from "react";
import StudentForm from "./components/StudentForm";
import StudentList from "./components/StudentList";
import StudentStats from "./components/StudentStats";
import ErrorBoundary from "./components/ErrorBoundary";
import Toast, { useToast } from "./components/Toast";
import { studentService, storageService } from "./services/api";
import "./App.css";

function AppContent() {
  const [students, setStudents] = useState([]);
  const [stats, setStats] = useState(null);
  const [storageInfo, setStorageInfo] = useState(null);
  const [editingStudent, setEditingStudent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);
  const { toasts, removeToast, success, error: showError, info } = useToast();

  const fetchStudents = useCallback(async () => {
    try {
      const response = await studentService.getAll();
      setStudents(response.data);
      setError(null);
    } catch (err) {
      const msg = err.response?.data?.error || err.message || "Failed to fetch students";
      setError(msg);
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchStats = useCallback(async () => {
    try {
      const response = await studentService.getStats();
      setStats(response.data);
    } catch (err) {
      console.error("Failed to fetch stats:", err);
    }
  }, []);

  const fetchStorageInfo = useCallback(async () => {
    try {
      const response = await storageService.getInfo();
      setStorageInfo(response.data);
    } catch (err) {
      console.error("Failed to fetch storage info:", err);
    }
  }, []);

  useEffect(() => {
    fetchStudents();
    fetchStats();
    fetchStorageInfo();
  }, [fetchStudents, fetchStats, fetchStorageInfo]);

  const handleStudentAdded = () => {
    fetchStudents();
    fetchStats();
    success("Student added successfully");
  };

  const handleStudentDeleted = () => {
    fetchStudents();
    fetchStats();
  };

  const handleEditStudent = (student) => {
    setEditingStudent(student);
  };

  const handleEditComplete = () => {
    setEditingStudent(null);
    fetchStudents();
    fetchStats();
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      const response = await storageService.save();
      success(response.data.message || "Data saved successfully");
    } catch (err) {
      showError(err.response?.data?.error || "Failed to save data");
    } finally {
      setSaving(false);
    }
  };

  const handleLoad = async () => {
    try {
      const response = await storageService.load();
      success(response.data.message || "Data loaded successfully");
      fetchStudents();
      fetchStats();
    } catch (err) {
      showError(err.response?.data?.error || "Failed to load data");
    }
  };

  if (loading) {
    return (
      <div className="app">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading students...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <Toast toasts={toasts} onRemove={removeToast} />

      <header className="app-header">
        <div className="header-content">
          <div>
            <h1>Student Grade Management System</h1>
          </div>
          <div className="header-actions">
            {storageInfo && (
              <div className="storage-badge">
                <span className="storage-dot"></span>
                {storageInfo.type === "localStorage" ? "Browser Storage" : storageInfo.type === "json" ? "JSON File" : "MySQL"} Storage
              </div>
            )}
            <button
              className="btn btn-header"
              onClick={handleSave}
              disabled={saving}
            >
              {saving ? "Saving..." : "Save"}
            </button>
            <button className="btn btn-header" onClick={handleLoad}>
              Load
            </button>
          </div>
        </div>
      </header>

      <main className="app-main">
        {error && (
          <div className="error-banner">
            <span className="alert-icon">!</span>
            {error}
            <button className="btn btn-small" onClick={fetchStudents}>
              Retry
            </button>
          </div>
        )}

        <div className="top-section">
          <StudentForm
            onStudentAdded={handleStudentAdded}
            editingStudent={editingStudent}
            onEditComplete={handleEditComplete}
          />
          <StudentStats stats={stats} />
        </div>

        <StudentList
          students={students}
          onStudentDeleted={handleStudentDeleted}
          onEditStudent={handleEditStudent}
          showToast={info}
        />
      </main>

      <footer className="app-footer">
        <p>Student Grade Management System - MVC Architecture</p>
      </footer>
    </div>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <AppContent />
    </ErrorBoundary>
  );
}

export default App;
