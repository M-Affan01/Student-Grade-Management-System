"""
Input Validation Module
========================
Provides comprehensive input validation and XSS protection for all
user-supplied data in the Student Grade Management System.

Validates student names, grades, emails (with domain whitelist),
subjects, and student IDs. Includes HTML escaping and script
injection prevention.


class Validator:
    Static utility class for input validation and sanitization.
    All methods are static and can be called without instantiation.
"""


import re
import html


class Validator:
    """Static utility class for input validation and XSS protection.

    Provides methods to validate individual fields (name, grade, email,
    subject) as well as complete student data dictionaries. Also includes
    sanitization and XSS detection utilities.

    Class Attributes:
        FORBIDDEN_PATTERNS (list): Regex patterns for XSS detection.
        VALID_DOMAINS (list): Whitelist of allowed email provider domains.
    """

    FORBIDDEN_PATTERNS = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'on\w+\s*=',
        r'<iframe',
        r'<object',
        r'<embed',
    ]

    VALID_DOMAINS = [
        "gmail.com", "yahoo.com", "yahoo.co.uk", "yahoo.co.in", "yahoo.ca", "yahoo.com.au",
        "hotmail.com", "hotmail.co.uk", "outlook.com", "outlook.co.uk", "live.com", "live.co.uk",
        "icloud.com", "me.com", "mac.com",
        "aol.com", "aim.com",
        "protonmail.com", "proton.me",
        "zoho.com", "mail.com", "email.com",
        "fastmail.com",
        "ymail.com",
        "rediffmail.com",
    ]

    @staticmethod
    def sanitize_input(value):
        """Sanitize a string input by HTML-escaping and stripping whitespace.

        Prevents XSS attacks by converting HTML special characters to
        their entity equivalents (e.g., '<' becomes '&lt;').

        Args:
            value: Input value. If not a string, returned as-is.

        Returns:
            str or original type: Sanitized string with HTML entities escaped
                and leading/trailing whitespace removed.
        """
        if not isinstance(value, str):
            return value
        value = html.escape(value)
        value = value.strip()
        return value

    @staticmethod
    def contains_xss(value):
        """Check if a string contains potential XSS attack patterns.

        Searches the value against known dangerous patterns including
        script tags, event handlers, and iframe/object/embed tags.

        Args:
            value: String to check. Non-strings return False.

        Returns:
            bool: True if a potentially dangerous pattern is detected,
                False otherwise.
        """
        if not isinstance(value, str):
            return False
        for pattern in Validator.FORBIDDEN_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                return True
        return False

    @staticmethod
    def validate_name(name):
        """Validate a student name.

        Rules:
            - Required (cannot be empty)
            - 2-100 characters long
            - Only letters, spaces, hyphens, apostrophes, and periods
            - No XSS patterns

        Args:
            name (str): Name to validate.

        Returns:
            tuple: (is_valid, error_message)
                - (True, "") if valid
                - (False, "specific error message") if invalid
        """
        if not name or not isinstance(name, str):
            return False, "Name is required"
        name = name.strip()
        if len(name) < 2:
            return False, "Name must be at least 2 characters"
        if len(name) > 100:
            return False, "Name must be less than 100 characters"
        if not re.match(r"^[a-zA-Z\s\-'.]+$", name):
            return False, "Name can only contain letters, spaces, hyphens, apostrophes"
        if Validator.contains_xss(name):
            return False, "Name contains invalid characters"
        return True, ""

    @staticmethod
    def validate_grade(grade):
        """Validate a numerical grade.

        Rules:
            - Required (cannot be None or empty)
            - Must be a valid number (int or float)
            - Between 0 and 100 inclusive
            - Maximum 2 decimal places

        Args:
            grade: Grade value to validate (int, float, or string).

        Returns:
            tuple: (is_valid, error_message)
                - (True, "") if valid
                - (False, "specific error message") if invalid
        """
        if grade is None or grade == "":
            return False, "Grade is required"
        try:
            grade = float(grade)
        except (TypeError, ValueError):
            return False, "Grade must be a valid number"
        if grade < 0:
            return False, "Grade cannot be negative"
        if grade > 100:
            return False, "Grade cannot exceed 100"
        if grade != int(grade) and len(str(grade).split(".")[1]) > 2:
            return False, "Grade can have at most 2 decimal places"
        return True, ""

    @staticmethod
    def validate_email(email):
        """Validate an email address with strict provider whitelisting.

        Rules:
            - Required (cannot be empty)
            - Max 150 characters
            - Must match standard email format (local@domain.tld)
            - Domain must be in VALID_DOMAINS whitelist (gmail.com, yahoo.com, etc.)
            - Local part must be at least 3 characters
            - Local part cannot start/end with dots or have consecutive dots
            - No XSS patterns

        Args:
            email (str): Email address to validate.

        Returns:
            tuple: (is_valid, error_message)
                - (True, "") if valid
                - (False, "specific error message") if invalid
        """
        if not email or email.strip() == "":
            return False, "Email is required"
        email = email.strip().lower()
        if len(email) > 150:
            return False, "Email must be less than 150 characters"

        pattern = r'^[a-z0-9._%+-]+@([a-z0-9.-]+\.[a-z]{2,})$'
        match = re.match(pattern, email)
        if not match:
            return False, "Invalid email format (e.g., student@gmail.com)"

        domain = match.group(1)
        if domain not in Validator.VALID_DOMAINS:
            allowed = ", ".join(Validator.VALID_DOMAINS[:5]) + "..."
            return False, f"Only real email providers allowed (e.g., {allowed})"

        local_part = email.split("@")[0]
        if len(local_part) < 3:
            return False, "Email username must be at least 3 characters"
        if local_part.startswith(".") or local_part.endswith("."):
            return False, "Email username cannot start or end with a dot"
        if ".." in local_part:
            return False, "Email username cannot have consecutive dots"

        if Validator.contains_xss(email):
            return False, "Email contains invalid characters"
        return True, ""

    @staticmethod
    def validate_subject(subject):
        """Validate a subject/course name.

        Rules:
            - Required (cannot be empty)
            - Max 100 characters
            - Only letters, spaces, and hyphens
            - No XSS patterns

        Args:
            subject (str): Subject name to validate.

        Returns:
            tuple: (is_valid, error_message)
                - (True, "") if valid
                - (False, "specific error message") if invalid
        """
        if not subject or subject.strip() == "":
            return False, "Subject is required"
        subject = subject.strip()
        if len(subject) > 100:
            return False, "Subject must be less than 100 characters"
        if not re.match(r"^[a-zA-Z\s\-]+$", subject):
            return False, "Subject can only contain letters, spaces, and hyphens"
        if Validator.contains_xss(subject):
            return False, "Subject contains invalid characters"
        return True, ""

    @staticmethod
    def validate_student_data(data):
        """Validate a complete student data dictionary.

        Validates all four fields (name, grade, email, subject) and
        returns all validation errors at once. All fields are required.

        Args:
            data (dict): Dictionary with student data.
                Expected keys: 'name', 'grade', 'email', 'subject'.

        Returns:
            tuple: (is_valid, errors_dict)
                - (True, {}) if all fields are valid
                - (False, {"field_name": "error_message", ...}) if any field is invalid
                - (False, {"general": "error"}) if data is not a valid dict
        """
        errors = {}

        if not data or not isinstance(data, dict):
            return False, {"general": "Invalid request data"}

        has_required = True

        if "name" not in data or not data.get("name", "").strip():
            errors["name"] = "Name is required"
            has_required = False
        else:
            valid, msg = Validator.validate_name(data["name"])
            if not valid:
                errors["name"] = msg

        if "grade" not in data or data.get("grade") == "" or data.get("grade") is None:
            errors["grade"] = "Grade is required"
            has_required = False
        else:
            valid, msg = Validator.validate_grade(data["grade"])
            if not valid:
                errors["grade"] = msg

        if "email" not in data or not data.get("email", "").strip():
            errors["email"] = "Email is required"
            has_required = False
        else:
            valid, msg = Validator.validate_email(data["email"])
            if not valid:
                errors["email"] = msg

        if "subject" not in data or not data.get("subject", "").strip():
            errors["subject"] = "Subject is required"
            has_required = False
        else:
            valid, msg = Validator.validate_subject(data["subject"])
            if not valid:
                errors["subject"] = msg

        return len(errors) == 0, errors

    @staticmethod
    def validate_id(student_id):
        """Validate a student ID.

        Rules:
            - Required (cannot be None)
            - Must be a valid integer
            - Must be positive (> 0)

        Args:
            student_id: Student ID to validate (int or string).

        Returns:
            tuple: (is_valid, error_message)
                - (True, "") if valid
                - (False, "specific error message") if invalid
        """
        if student_id is None:
            return False, "Student ID is required"
        try:
            student_id = int(student_id)
        except (TypeError, ValueError):
            return False, "Student ID must be a number"
        if student_id <= 0:
            return False, "Student ID must be positive"
        return True, ""
