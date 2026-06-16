import React, { useState } from "react";
import { studentService } from "../services/api";
import ConfirmDialog from "./ConfirmDialog";

function StudentList({ students, onStudentDeleted, onEditStudent, showToast }) {
  const [sortBy, setSortBy] = useState("id");
  const [sortOrder, setSortOrder] = useState("asc");
  const [searchTerm, setSearchTerm] = useState("");
  const [deletingId, setDeletingId] = useState(null);
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [pendingDelete, setPendingDelete] = useState(null);

  const handleDeleteClick = (id, name) => {
    setPendingDelete({ id, name });
    setConfirmOpen(true);
  };

  const handleDeleteConfirm = async () => {
    if (!pendingDelete) return;
    setConfirmOpen(false);
    setDeletingId(pendingDelete.id);
    try {
      const response = await studentService.delete(pendingDelete.id);
      showToast(response.data.message || "Student deleted", "success");
      onStudentDeleted();
    } catch (err) {
      const msg = err.response?.data?.error || "Failed to delete student";
      showToast(msg, "error");
    } finally {
      setDeletingId(null);
      setPendingDelete(null);
    }
  };

  const handleDeleteCancel = () => {
    setConfirmOpen(false);
    setPendingDelete(null);
  };

  const getLetterGrade = (grade) => {
    if (grade >= 90) return "A";
    if (grade >= 80) return "B";
    if (grade >= 70) return "C";
    if (grade >= 60) return "D";
    return "F";
  };

  const getGradeClass = (grade) => {
    if (grade >= 90) return "grade-a";
    if (grade >= 80) return "grade-b";
    if (grade >= 70) return "grade-c";
    if (grade >= 60) return "grade-d";
    return "grade-f";
  };

  const filteredStudents = students
    .filter((s) =>
      s.name.toLowerCase().includes(searchTerm.toLowerCase())
    )
    .sort((a, b) => {
      let comparison = 0;
      if (sortBy === "id") {
        comparison = a.id - b.id;
      } else if (sortBy === "name") {
        comparison = a.name.localeCompare(b.name);
      } else if (sortBy === "grade") {
        comparison = a.grade - b.grade;
      }
      return sortOrder === "asc" ? comparison : -comparison;
    });

  return (
    <div className="card">
      <ConfirmDialog
        open={confirmOpen}
        title="Delete Student"
        message={pendingDelete ? `Are you sure you want to delete "${pendingDelete.name}"? This action cannot be undone.` : ""}
        onConfirm={handleDeleteConfirm}
        onCancel={handleDeleteCancel}
      />
      <h2>Student List ({filteredStudents.length})</h2>

      <div className="controls">
        <div className="search-box">
          <input
            type="text"
            placeholder="Search by name..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            maxLength={100}
          />
          {searchTerm && (
            <span className="search-count">
              {filteredStudents.length} result(s)
            </span>
          )}
        </div>
        <div className="sort-controls">
          <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
            <option value="id">Sort by ID</option>
            <option value="name">Sort by Name</option>
            <option value="grade">Sort by Grade</option>
          </select>
          <button
            className="btn btn-small"
            onClick={() => setSortOrder(sortOrder === "asc" ? "desc" : "asc")}
          >
            {sortOrder === "asc" ? "↑ Asc" : "↓ Desc"}
          </button>
        </div>
      </div>

      {filteredStudents.length === 0 ? (
        <div className="no-data">
          {searchTerm ? (
            <p>No students match "{searchTerm}"</p>
          ) : (
            <p>No students yet. Add one above!</p>
          )}
        </div>
      ) : (
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Grade</th>
                <th>Letter</th>
                <th>Subject</th>
                <th>Email</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredStudents.map((student) => (
                <tr key={student.id}>
                  <td>{student.id}</td>
                  <td>{student.name}</td>
                  <td className={getGradeClass(student.grade)}>
                    {student.grade}
                  </td>
                  <td>
                    <span
                      className={`letter-grade ${getGradeClass(student.grade)}`}
                    >
                      {getLetterGrade(student.grade)}
                    </span>
                  </td>
                  <td>{student.subject || "-"}</td>
                  <td>{student.email || "-"}</td>
                  <td className="actions-cell">
                    <button
                      className="btn btn-edit"
                      onClick={() => { onEditStudent(student); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
                      disabled={deletingId === student.id}
                    >
                      Edit
                    </button>
                    <button
                      className="btn btn-delete"
                      onClick={() => handleDeleteClick(student.id, student.name)}
                      disabled={deletingId === student.id}
                    >
                      {deletingId === student.id ? "..." : "Delete"}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default StudentList;
