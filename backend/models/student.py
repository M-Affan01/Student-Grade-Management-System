"""
Student Model Module
====================
Defines the Student class which represents a single student entity
in the Student Grade Management System. Uses encapsulation with
properties and validation on setters.


class Student:
    Represents a student with name, grade, email, and subject.
    Enforces validation rules on name and grade via property setters.

    Attributes:
        id (int): Unique identifier for the student (auto-assigned by storage).
        name (str): Full name of the student (2-100 chars, letters only).
        grade (float): Numerical grade between 0 and 100.
        email (str): Email address (must be from a valid provider).
        subject (str): Subject/course name.
"""


class Student:
    """A single student entity with validated properties.

    Attributes (private, accessed via properties):
        _id (int or None): Auto-assigned unique identifier.
        _name (str): Student's full name, validated on set.
        _grade (float): Student's grade (0-100), validated on set.
        _email (str): Student's email address.
        _subject (str): Student's subject/course.
    """

    def __init__(self, student_id=None, name="", grade=0, email="", subject=""):
        """Initialize a Student instance.

        Args:
            student_id (int or None): Unique ID, typically assigned by storage layer.
                Defaults to None (auto-assigned on save).
            name (str): Full name of the student. Must be 2-100 characters.
            grade (int or float): Numerical grade between 0 and 100.
            email (str): Email address of the student. Must be from a valid provider.
            subject (str): Subject or course name.

        Returns:
            None
        """
        self._id = student_id
        self._name = name
        self._grade = grade
        self._email = email
        self._subject = subject

    @property
    def id(self):
        """Get the student's unique identifier.

        Returns:
            int or None: The student's ID, or None if not yet assigned.
        """
        return self._id

    @id.setter
    def id(self, value):
        """Set the student's unique identifier.

        Args:
            value (int): The new ID value.

        Returns:
            None
        """
        self._id = value

    @property
    def name(self):
        """Get the student's name.

        Returns:
            str: The student's full name.
        """
        return self._name

    @name.setter
    def name(self, value):
        """Set the student's name with validation.

        Args:
            value (str): New name. Must be non-empty after stripping whitespace.

        Raises:
            ValueError: If value is empty or whitespace-only.

        Returns:
            None
        """
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()

    @property
    def grade(self):
        """Get the student's grade as a float.

        Returns:
            float: The student's numerical grade (0-100).
        """
        return float(self._grade) if self._grade is not None else 0

    @grade.setter
    def grade(self, value):
        """Set the student's grade with validation.

        Args:
            value (int or float): New grade between 0 and 100 inclusive.

        Raises:
            ValueError: If grade is outside the 0-100 range.

        Returns:
            None
        """
        value = float(value)
        if value < 0 or value > 100:
            raise ValueError("Grade must be between 0 and 100")
        self._grade = value

    @property
    def email(self):
        """Get the student's email address.

        Returns:
            str: The student's email.
        """
        return self._email

    @email.setter
    def email(self, value):
        """Set the student's email address.

        Args:
            value (str): New email address.

        Returns:
            None
        """
        self._email = value

    @property
    def subject(self):
        """Get the student's subject.

        Returns:
            str: The subject/course name.
        """
        return self._subject

    @subject.setter
    def subject(self, value):
        """Set the student's subject.

        Args:
            value (str): New subject name.

        Returns:
            None
        """
        self._subject = value

    def to_dict(self):
        """Convert the student to a dictionary for JSON serialization.

        Returns:
            dict: Dictionary with keys 'id', 'name', 'grade', 'email', 'subject'.
                Grade is always returned as a float. ID may be None.
        """
        return {
            "id": int(self._id) if self._id is not None else None,
            "name": self._name,
            "grade": float(self._grade) if self._grade is not None else 0,
            "email": self._email,
            "subject": self._subject
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Student instance from a dictionary.

        Used to deserialize data from JSON files or MySQL query results.
        Gracefully handles missing keys with defaults.

        Args:
            data (dict): Dictionary containing student data.
                Expected keys: 'id', 'name', 'grade', 'email', 'subject'.

        Returns:
            Student: A new Student instance populated from the dictionary.
        """
        return cls(
            student_id=data.get("id"),
            name=data.get("name", ""),
            grade=float(data.get("grade", 0)),
            email=data.get("email", ""),
            subject=data.get("subject", "")
        )

    def get_letter_grade(self):
        """Convert numerical grade to a letter grade.

        Grading scale:
            A: 90-100
            B: 80-89
            C: 70-79
            D: 60-69
            F: Below 60

        Returns:
            str: Single letter grade ('A', 'B', 'C', 'D', or 'F').
        """
        if self._grade >= 90:
            return "A"
        elif self._grade >= 80:
            return "B"
        elif self._grade >= 70:
            return "C"
        elif self._grade >= 60:
            return "D"
        else:
            return "F"

    def is_passing(self):
        """Check if the student is passing (grade >= 60).

        Returns:
            bool: True if grade is 60 or above, False otherwise.
        """
        return self._grade >= 60

    def __str__(self):
        """Human-readable string representation.

        Returns:
            str: Format: Student(id=X, name='Y', grade=Z)
        """
        return f"Student(id={self._id}, name='{self._name}', grade={self._grade})"

    def __repr__(self):
        """Developer representation (same as __str__).

        Returns:
            str: Same format as __str__.
        """
        return self.__str__()
