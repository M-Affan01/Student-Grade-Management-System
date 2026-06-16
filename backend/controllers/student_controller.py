"""
Student Controller Module (MVC - Controller)
=============================================
Handles all HTTP request routing for the Student Grade Management System.
Defines Flask Blueprint routes for CRUD operations, search, sort, stats,
and index-based operations on student data.

Each route handler validates input, interacts with the storage backend
via current_app.storage, and returns standardized JSON responses.


student_bp: Flask Blueprint containing all student-related API routes.
_get_storage(): Helper to access the app's storage backend.
_ok(message, data, status): Helper for success JSON responses.
_err(message, details, status): Helper for error JSON responses.
"""


import traceback
from flask import Blueprint, request, jsonify, current_app
from models.student import Student
from utils.validator import Validator
from views.response import (
    student_to_dict, student_list_to_dict,
    success_response, error_response,
    stats_view, sort_view, search_view, storage_info_view
)

# Flask Blueprint for all student-related routes
student_bp = Blueprint("students", __name__)


def _get_storage():
    """Get the storage backend from Flask's current_app context.

    Returns:
        JSONStorage or MySQLStorage: The active storage backend.
    """
    return current_app.storage


def _ok(message, data=None, status=200):
    """Create a success JSON response with status code.

    Args:
        message (str): Success message.
        data (dict or None): Additional data to include. Defaults to None.
        status (int): HTTP status code. Defaults to 200.

    Returns:
        tuple: (jsonified_response, status_code) for Flask.
    """
    return jsonify(success_response(message, data)[0]), status


def _err(message, details=None, status=400):
    """Create an error JSON response with status code.

    Args:
        message (str): Error message.
        details (dict or None): Additional error details. Defaults to None.
        status (int): HTTP status code. Defaults to 400.

    Returns:
        tuple: (jsonified_response, status_code) for Flask.
    """
    return jsonify(error_response(message, details, status)[0]), status


# ─── GET ALL STUDENTS ─────────────────────────────────────────────────────

@student_bp.route("/api/students", methods=["GET"])
def get_students():
    """Retrieve all students from storage.

    GET /api/students

    Returns:
        JSON array of student objects, or error response.
    """
    try:
        storage = _get_storage()
        students = storage.get_all()
        return jsonify(student_list_to_dict(students))
    except Exception as e:
        return _err("Failed to retrieve students", str(e), 500)


# ─── GET STUDENT BY ID ────────────────────────────────────────────────────

@student_bp.route("/api/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    """Retrieve a single student by their unique ID.

    GET /api/students/<student_id>

    Args:
        student_id (int): The student's unique identifier.

    Returns:
        JSON object of the student, or 404 error if not found.
    """
    try:
        storage = _get_storage()
        student = storage.get_by_id(student_id)
        if student:
            return jsonify(student_to_dict(student))
        return _err(f"Student with ID {student_id} not found", status=404)
    except Exception as e:
        return _err("Failed to retrieve student", str(e), 500)


# ─── ADD NEW STUDENT ──────────────────────────────────────────────────────

@student_bp.route("/api/students", methods=["POST"])
def add_student():
    """Add a new student to the system.

    POST /api/students
    Body: JSON with 'name', 'grade', 'email', 'subject' (all required).

    Validates all fields, checks for duplicates, sanitizes input,
    then saves to storage. Returns the created student with new ID.

    Returns:
        JSON with 'message' and 'student' object, status 201 on success.
        Status 400 for validation errors, 409 for duplicates.
    """
    try:
        storage = _get_storage()
        data = request.get_json(silent=True)
        if data is None:
            return _err("Invalid JSON", {"general": "Request body must be valid JSON"})

        valid, errors = Validator.validate_student_data(data)
        if not valid:
            return _err("Validation failed", errors)

        name = Validator.sanitize_input(data["name"])
        grade = float(data["grade"])
        email = Validator.sanitize_input(data.get("email", ""))
        subject = Validator.sanitize_input(data.get("subject", ""))

        existing = storage.search(name)
        if existing and any(s.name.lower() == name.lower() for s in existing):
            return _err("Duplicate student", {"name": f"A student named '{name}' already exists"}, 409)

        student = Student(name=name, grade=grade, email=email, subject=subject)
        result = storage.add(student)   
        # yahan sa json ma jaega as a list add
        if result:
            return _ok("Student added successfully", {"student": result.to_dict()}, 201)
        return _err("Failed to add student", status=500)
    except ValueError as e:
        return _err("Invalid data", {"grade": str(e)})
    except Exception as e:
        traceback.print_exc()
        return _err("Failed to add student", str(e), 500)


# ─── UPDATE STUDENT BY ID ─────────────────────────────────────────────────

@student_bp.route("/api/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """Update an existing student's data by ID.

    PUT /api/students/<student_id>
    Body: JSON with any of 'name', 'grade', 'email', 'subject'.

    Validates input, checks for duplicate names, and updates only
    the provided fields.

    Args:
        student_id (int): The student's unique identifier.

    Returns:
        JSON with 'message' and updated 'student' object.
        Status 404 if student not found, 409 for duplicate names.
    """
    try:
        storage = _get_storage()
        student = storage.get_by_id(student_id)
        if not student:
            return _err(f"Student with ID {student_id} not found", status=404)

        data = request.get_json(silent=True)
        if data is None:
            return _err("Invalid JSON")

        valid, errors = Validator.validate_student_data(data)
        if not valid:
            return _err("Validation failed", errors)

        if "name" in data:
            new_name = Validator.sanitize_input(data["name"])
            existing = storage.search(new_name)
            if existing and any(s.id != student_id and s.name.lower() == new_name.lower() for s in existing):
                return _err("Duplicate student", {"name": f"A student named '{new_name}' already exists"}, 409)
            student.name = new_name

        if "grade" in data:
            student.grade = float(data["grade"])
        if "email" in data:
            student.email = Validator.sanitize_input(data["email"])
        if "subject" in data:
            student.subject = Validator.sanitize_input(data["subject"])

        if storage.update(student):
            return _ok("Student updated successfully", {"student": student.to_dict()})
        return _err("Failed to update student", status=500)
    except ValueError as e:
        return _err("Invalid data", {"grade": str(e)})
    except Exception as e:
        traceback.print_exc()
        return _err("Failed to update student", str(e), 500)


# ─── DELETE STUDENT BY ID ─────────────────────────────────────────────────

@student_bp.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """Delete a student by their unique ID.

    DELETE /api/students/<student_id>

    Args:
        student_id (int): The student's unique identifier.

    Returns:
        JSON with 'message' on success, or 404 error if not found.
    """
    try:
        storage = _get_storage()
        student = storage.get_by_id(student_id)
        if not student:
            return _err(f"Student with ID {student_id} not found", status=404)

        if storage.delete(student_id):
            return _ok(f"Student '{student.name}' deleted successfully")
        return _err("Failed to delete student", status=500)
    except Exception as e:
        traceback.print_exc()
        return _err("Failed to delete student", str(e), 500)


# ─── SEARCH STUDENTS BY NAME ──────────────────────────────────────────────

@student_bp.route("/api/students/search", methods=["GET"])
def search_students():
    """Search students by name (case-insensitive partial match).

    GET /api/students/search?name=<query>

    Query Params:
        name (str): Search substring. Max 100 characters.

    Returns:
        JSON with 'results' array, 'count', and 'query'.
    """
    try:
        storage = _get_storage()
        name = request.args.get("name", "").strip()
        if len(name) > 100:
            return _err("Search query too long")

        name = Validator.sanitize_input(name)
        results = storage.search(name)
        return jsonify(search_view(results, name))
    except Exception as e:
        return _err("Search failed", str(e), 500)


# ─── GET STATISTICS ───────────────────────────────────────────────────────

@student_bp.route("/api/students/stats", methods=["GET"])
def get_stats():
    """Get comprehensive class statistics.

    GET /api/students/stats

    Returns:
        JSON with total_students, average_grade, highest_grade,
        lowest_grade, passing, failing, and grade distribution.
    """
    try:
        storage = _get_storage()
        return jsonify(stats_view(storage.get_stats()))
    except Exception as e:
        return _err("Failed to calculate stats", str(e), 500)


# ─── SORT STUDENTS BY GRADE ──────────────────────────────────────────────

@student_bp.route("/api/students/sort", methods=["GET"])
def sort_by_grade():
    """Get all students sorted by grade.

    GET /api/students/sort?ascending=true

    Query Params:
        ascending (str): 'true' for lowest-to-highest, 'false' for
            highest-to-lowest. Defaults to 'true'.

    Returns:
        JSON with 'students' array, 'ascending' flag, and 'count'.
    """
    try:
        storage = _get_storage()
        ascending = request.args.get("ascending", "true").lower() == "true"
        students = storage.sort_by_grade(ascending=ascending)
        return jsonify(sort_view(students, ascending))
    except Exception as e:
        return _err("Failed to sort students", str(e), 500)


# ─── INDEX-BASED OPERATIONS ───────────────────────────────────────────────

@student_bp.route("/api/students/index/<int:index>", methods=["GET"])
def get_student_by_index(index):
    """Get a student by their list position (0-based).

    GET /api/students/index/<index>

    Args:
        index (int): Zero-based position in the sorted list.

    Returns:
        JSON student object, or error if index is out of range.
    """
    try:
        storage = _get_storage()
        if index < 0 or index >= storage.size():
            return _err(f"Index {index} out of range")
        student = storage.get_by_index(index)
        if student:
            return jsonify(student_to_dict(student))
        return _err(f"No student at index {index}", status=404)
    except Exception as e:
        return _err("Failed to retrieve student", str(e), 500)


@student_bp.route("/api/students/index/<int:index>", methods=["DELETE"])
def delete_student_by_index(index):
    """Delete a student by their list position (0-based).

    DELETE /api/students/index/<index>

    Args:
        index (int): Zero-based position in the list.

    Returns:
        JSON with 'message' on success, or error if index is invalid.
    """
    try:
        storage = _get_storage()
        if index < 0 or index >= storage.size():
            return _err(f"Index {index} out of range")
        removed = storage.delete_by_index(index)
        if removed:
            return _ok(f"Student '{removed.name}' deleted successfully")
        return _err(f"No student at index {index}", status=404)
    except Exception as e:
        traceback.print_exc()
        return _err("Failed to delete student", str(e), 500)


@student_bp.route("/api/students/index/<int:index>/grade", methods=["PUT"])
def update_grade_by_index(index):
    """Update only the grade of a student at a given index.

    PUT /api/students/index/<index>/grade
    Body: JSON with 'grade' field.

    Args:
        index (int): Zero-based position of the student.

    Returns:
        JSON with 'message' and updated 'student' object.
    """
    try:
        storage = _get_storage()
        if index < 0 or index >= storage.size():
            return _err(f"Index {index} out of range")

        data = request.get_json(silent=True)
        if data is None:
            return _err("Invalid JSON")

        if "grade" not in data:
            return _err("grade is required")

        valid, msg = Validator.validate_grade(data["grade"])
        if not valid:
            return _err(msg)

        student = storage.get_by_index(index)
        if student:
            student.grade = float(data["grade"])
            if storage.update(student):
                return _ok("Grade updated successfully", {"student": student.to_dict()})
        return _err("Failed to update grade", status=500)
    except ValueError as e:
        return _err("Invalid grade", str(e))
    except Exception as e:
        traceback.print_exc()
        return _err("Failed to update grade", str(e), 500)


# ─── STATISTICS ENDPOINTS ─────────────────────────────────────────────────

@student_bp.route("/api/students/size", methods=["GET"])
def get_size():
    """Get the total number of students.

    GET /api/students/size

    Returns:
        JSON with 'size' integer.
    """
    try:
        storage = _get_storage()
        return jsonify({"size": storage.size()})
    except Exception as e:
        return _err("Failed to get size", str(e), 500)


@student_bp.route("/api/students/average", methods=["GET"])
def get_average():
    """Get the average grade across all students.

    GET /api/students/average

    Returns:
        JSON with 'average' float.
    """
    try:
        storage = _get_storage()
        stats = storage.get_stats()
        return jsonify({"average": stats["average_grade"]})
    except Exception as e:
        return _err("Failed to calculate average", str(e), 500)


@student_bp.route("/api/students/highest", methods=["GET"])
def get_highest():
    """Get the highest grade among all students.

    GET /api/students/highest

    Returns:
        JSON with 'highest' float.
    """
    try:
        storage = _get_storage()
        stats = storage.get_stats()
        return jsonify({"highest": stats["highest_grade"]})
    except Exception as e:
        return _err("Failed to get highest grade", str(e), 500)


@student_bp.route("/api/students/lowest", methods=["GET"])
def get_lowest():
    """Get the lowest grade among all students.

    GET /api/students/lowest

    Returns:
        JSON with 'lowest' float.
    """
    try:
        storage = _get_storage()
        stats = storage.get_stats()
        return jsonify({"lowest": stats["lowest_grade"]})
    except Exception as e:
        return _err("Failed to get lowest grade", str(e), 500)
