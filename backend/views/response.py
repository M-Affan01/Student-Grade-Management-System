"""
Response View Module (MVC - View)
==================================
Provides standardized response formatting functions for the Flask API.
Ensures consistent JSON response structures across all endpoints.


student_to_dict(student): Convert a single student to dict.
student_list_to_dict(students): Convert a list of students to dicts.
success_response(message, data, status): Format a success response.
error_response(message, details, status): Format an error response.
stats_view(stats): Format statistics for API response.
sort_view(students, ascending): Format sorted student list response.
search_view(results, query): Format search results response.
storage_info_view(storage_type, storage): Format storage info response.
"""


from models.student import Student


def student_to_dict(student):
    """Convert a Student object to a dictionary for JSON serialization.

    Args:
        student (Student): The Student object to convert.

    Returns:
        dict: Dictionary with id, name, grade, email, subject keys.
    """
    return student.to_dict()


def student_list_to_dict(students):
    """Convert a list of Student objects to a list of dictionaries.

    Args:
        students (list): List of Student objects.

    Returns:
        list: List of dictionaries, one per student.
    """
    return [s.to_dict() for s in students]


def success_response(message, data=None, status=200):
    """Build a standardized success response dictionary.

    Args:
        message (str): Success message describing the operation.
        data (dict or None): Additional data to merge into the response.
            Defaults to None (no extra data).
        status (int): HTTP status code. Defaults to 200.

    Returns:
        tuple: (response_dict, status_code)
            response_dict always contains 'message' key.
    """
    response = {"message": message}
    if data:
        response.update(data)
    return response, status


def error_response(message, details=None, status=400):
    """Build a standardized error response dictionary.

    Args:
        message (str): Error message describing what went wrong.
        details (dict or str or None): Additional error details such as
            field-level validation errors. Defaults to None.
        status (int): HTTP status code. Defaults to 400.

    Returns:
        tuple: (response_dict, status_code)
            response_dict always contains 'error' key, and 'details' if provided.
    """
    response = {"error": message}
    if details:
        response["details"] = details
    return response, status


def stats_view(stats):
    """Format class statistics for API response.

    Maps the statistics dictionary from the storage layer to a
    clean API-compatible format.

    Args:
        stats (dict): Raw statistics from storage.get_stats().
            Keys: total_students, average_grade, highest_grade,
            lowest_grade, passing, failing, grade_a-f.

    Returns:
        dict: Formatted statistics dictionary with all numeric values.
    """
    return {
        "total_students": stats["total_students"],
        "average_grade": stats["average_grade"],
        "highest_grade": stats["highest_grade"],
        "lowest_grade": stats["lowest_grade"],
        "passing": stats["passing"],
        "failing": stats["failing"],
        "grade_a": stats["grade_a"],
        "grade_b": stats["grade_b"],
        "grade_c": stats["grade_c"],
        "grade_d": stats["grade_d"],
        "grade_f": stats["grade_f"]
    }


def sort_view(students, ascending):
    """Format a sorted student list for API response.

    Args:
        students (list): Sorted list of Student objects.
        ascending (bool): Sort direction used (True = ascending).

    Returns:
        dict: Dictionary with 'students' (list of dicts),
            'ascending' (bool), and 'count' (int).
    """
    return {
        "students": student_list_to_dict(students),
        "ascending": ascending,
        "count": len(students)
    }


def search_view(results, query):
    """Format search results for API response.

    Args:
        results (list): List of matching Student objects.
        query (str): The search query that was used.

    Returns:
        dict: Dictionary with 'results' (list of dicts),
            'count' (int), and 'query' (str).
    """
    return {
        "results": student_list_to_dict(results),
        "count": len(results),
        "query": query
    }


def storage_info_view(storage_type, storage):
    """Format storage backend information for API response.

    Provides type-specific details: filepath for JSON, connection
    status and database name for MySQL.

    Args:
        storage_type (str): 'json' or 'mysql'.
        storage: The active storage backend instance.

    Returns:
        dict: Storage info with 'type', 'students_count', and
            type-specific fields (filepath/connected/database).
    """
    info = {"type": storage_type, "students_count": storage.size()}
    if storage_type == "json":
        import os
        info["filepath"] = storage.filepath
        info["file_exists"] = os.path.exists(storage.filepath)
    elif storage_type == "mysql":
        info["connected"] = storage.is_connected()
        info["database"] = storage.config.get("database", "")
    return info
