import React, { useState, useEffect, useCallback } from "react";
import { studentService } from "../services/api";

const VALID_EMAIL_DOMAINS = [
  "gmail.com", "yahoo.com", "yahoo.co.uk", "yahoo.co.in", "yahoo.ca", "yahoo.com.au",
  "hotmail.com", "hotmail.co.uk", "outlook.com", "outlook.co.uk", "live.com", "live.co.uk",
  "icloud.com", "me.com", "mac.com",
  "aol.com", "aim.com",
  "protonmail.com", "proton.me",
  "zoho.com", "mail.com", "email.com",
  "fastmail.com", "ymail.com", "rediffmail.com",
];

const VALIDATION_RULES = {
  name: {
    required: true,
    minLength: 2,
    maxLength: 100,
    pattern: /^[a-zA-Z\s\-'.]+$/,
    messages: {
      required: "Name is required",
      minLength: "Name must be at least 2 characters",
      maxLength: "Name must be less than 100 characters",
      pattern: "Name can only contain letters, spaces, hyphens",
    },
  },
  grade: {
    required: true,
    min: 0,
    max: 100,
    messages: {
      required: "Grade is required",
      min: "Grade cannot be negative",
      max: "Grade cannot exceed 100",
      nan: "Grade must be a valid number",
    },
  },
  email: {
    required: true,
    maxLength: 150,
    messages: {
      required: "Email is required",
      format: "Invalid email format (e.g., student@gmail.com)",
      domain: "Only real email providers allowed (e.g., gmail.com, yahoo.com)",
      minLength: "Email username must be at least 3 characters",
      dots: "Email username cannot start/end with dots or have consecutive dots",
      maxLength: "Email must be less than 150 characters",
    },
  },
  subject: {
    required: true,
    maxLength: 100,
    pattern: /^[a-zA-Z\s\-]+$/,
    messages: {
      required: "Subject is required",
      maxLength: "Subject must be less than 100 characters",
      pattern: "Subject can only contain letters, spaces, and hyphens",
    },
  },
};

function validateField(name, value) {
  const rules = VALIDATION_RULES[name];
  if (!rules) return "";

  const trimmed = typeof value === "string" ? value.trim() : value;

  if (rules.required && (trimmed === "" || trimmed === null || trimmed === undefined)) {
    return rules.messages.required;
  }

  if (!rules.required && trimmed === "") return "";

  if (name === "grade") {
    const num = parseFloat(trimmed);
    if (isNaN(num)) return rules.messages.nan;
    if (num < rules.min) return rules.messages.min;
    if (num > rules.max) return rules.messages.max;
  }

  if (name === "email" && trimmed !== "") {
    const email = trimmed.toLowerCase();
    if (email.length > 150) return rules.messages.maxLength;

    const emailPattern = /^[a-z0-9._%+-]+@([a-z0-9.-]+\.[a-z]{2,})$/;
    const match = email.match(emailPattern);
    if (!match) return rules.messages.format;

    const domain = match[1];
    if (!VALID_EMAIL_DOMAINS.includes(domain)) return rules.messages.domain;

    const localPart = email.split("@")[0];
    if (localPart.length < 3) return rules.messages.minLength;
    if (localPart.startsWith(".") || localPart.endsWith(".")) return rules.messages.dots;
    if (localPart.includes("..")) return rules.messages.dots;

    return "";
  }

  if (rules.minLength && trimmed.length < rules.minLength) {
    return rules.messages.minLength;
  }

  if (rules.maxLength && trimmed.length > rules.maxLength) {
    return rules.messages.maxLength;
  }

  if (rules.pattern && trimmed !== "" && !rules.pattern.test(trimmed)) {
    return rules.messages.pattern;
  }

  return "";
}

function StudentForm({ onStudentAdded, editingStudent, onEditComplete }) {
  const [formData, setFormData] = useState({
    name: "",
    grade: "",
    email: "",
    subject: "",
  });
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});
  const [serverError, setServerError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");

  useEffect(() => {
    if (editingStudent) {
      setFormData({
        name: editingStudent.name || "",
        grade: editingStudent.grade?.toString() || "",
        email: editingStudent.email || "",
        subject: editingStudent.subject || "",
      });
      setErrors({});
      setTouched({});
      setServerError("");
    }
  }, [editingStudent]);

  const validateAll = useCallback(() => {
    const newErrors = {};
    Object.keys(formData).forEach((field) => {
      const error = validateField(field, formData[field]);
      if (error) newErrors[field] = error;
    });
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }, [formData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    setServerError("");
    setSuccessMessage("");

    if (touched[name]) {
      const error = validateField(name, value);
      setErrors((prev) => ({ ...prev, [name]: error }));
    }
  };

  const handleBlur = (e) => {
    const { name, value } = e.target;
    setTouched((prev) => ({ ...prev, [name]: true }));
    const error = validateField(name, value);
    setErrors((prev) => ({ ...prev, [name]: error }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setServerError("");
    setSuccessMessage("");

    const allTouched = {};
    Object.keys(formData).forEach((key) => (allTouched[key] = true));
    setTouched(allTouched);

    if (!validateAll()) return;

    setIsSubmitting(true);
    try {
      const data = {
        name: formData.name.trim(),
        grade: parseFloat(formData.grade),
        email: formData.email.trim(),
        subject: formData.subject.trim(),
      };

      let response;
      if (editingStudent) {
        response = await studentService.update(editingStudent.id, data);
        setSuccessMessage(response.data.message || "Student updated successfully");
        setTimeout(() => onEditComplete(), 1500);
      } else {
        response = await studentService.create(data);
        setSuccessMessage(response.data.message || "Student added successfully");
        setFormData({ name: "", grade: "", email: "", subject: "" });
        setTouched({});
        setErrors({});
        setTimeout(() => {
          setSuccessMessage("");
          onStudentAdded();
        }, 1500);
      }
    } catch (err) {
      if (err.response?.data?.details) {
        setErrors(err.response.data.details);
      } else if (err.response?.data?.error) {
        setServerError(err.response.data.error);
      } else if (err.code === "ECONNABORTED") {
        setServerError("Request timed out. Please try again.");
      } else if (!err.response) {
        setServerError("Cannot connect to server. Is the backend running?");
      } else {
        setServerError("An unexpected error occurred");
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCancel = () => {
    setFormData({ name: "", grade: "", email: "", subject: "" });
    setErrors({});
    setTouched({});
    setServerError("");
    setSuccessMessage("");
    onEditComplete();
  };

  const getFieldClassName = (fieldName) => {
    if (errors[fieldName] && touched[fieldName]) return "form-input error";
    if (!errors[fieldName] && touched[fieldName]) return "form-input valid";
    return "form-input";
  };

  return (
    <div className="card">
      <h2>{editingStudent ? "Edit Student" : "Add New Student"}</h2>

      {serverError && (
        <div className="alert alert-error">
          <span className="alert-icon">!</span>
          {serverError}
        </div>
      )}

      {successMessage && (
        <div className="alert alert-success">
          <span className="alert-icon">✓</span>
          {successMessage}
        </div>
      )}

      <form onSubmit={handleSubmit} noValidate>
        <div className="form-group">
          <label htmlFor="name">
            Name <span className="required">*</span>
          </label>
          <input
            id="name"
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            onBlur={handleBlur}
            className={getFieldClassName("name")}
            placeholder="Enter student name"
            autoComplete="name"
          />
          {errors.name && touched.name && (
            <span className="field-error">{errors.name}</span>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="grade">
            Grade (0-100) <span className="required">*</span>
          </label>
          <input
            id="grade"
            type="number"
            name="grade"
            value={formData.grade}
            onChange={handleChange}
            onBlur={handleBlur}
            className={getFieldClassName("grade")}
            min="0"
            max="100"
            step="1"
            placeholder="Enter grade"
          />
          {errors.grade && touched.grade && (
            <span className="field-error">{errors.grade}</span>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="email">
            Email <span className="required">*</span>
          </label>
          <input
            id="email"
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            onBlur={handleBlur}
            className={getFieldClassName("email")}
            placeholder="Enter email"
            autoComplete="email"
          />
          {errors.email && touched.email && (
            <span className="field-error">{errors.email}</span>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="subject">
            Subject <span className="required">*</span>
          </label>
          <input
            id="subject"
            type="text"
            name="subject"
            value={formData.subject}
            onChange={handleChange}
            onBlur={handleBlur}
            className={getFieldClassName("subject")}
            placeholder="Enter subject"
          />
          {errors.subject && touched.subject && (
            <span className="field-error">{errors.subject}</span>
          )}
        </div>

        <div className="button-group">
          <button
            type="submit"
            className="btn btn-primary"
            disabled={isSubmitting}
          >
            {isSubmitting
              ? "Saving..."
              : editingStudent
              ? "Update Student"
              : "Add Student"}
          </button>
          {editingStudent && (
            <button
              type="button"
              className="btn btn-secondary"
              onClick={handleCancel}
              disabled={isSubmitting}
            >
              Cancel
            </button>
          )}
        </div>
      </form>
    </div>
  );
}

export default StudentForm;
