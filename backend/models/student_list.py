"""
Student List ADT Module
========================
Implements a List Abstract Data Type (ADT) for managing a collection
of Student objects. Provides operations for add, remove, update, search,
sort, and statistical analysis of student data.


class StudentList:
    List ADT implementation for Student objects.
    Supports CRUD operations, search, sort, and statistics.
"""


from models.student import Student


class StudentList:
    """List ADT for managing a collection of Student objects.

    Provides index-based access, search, sort, and statistical operations
    on an in-memory list of students. Used as the core data structure
    for the grade management system.

    Attributes:
        _students (list): Internal list of Student objects.
    """

    def __init__(self):
        """Initialize an empty StudentList.

        Creates a new empty list to hold Student objects.

        Returns:
            None
        """
        self._students = []

    def add_student(self, name, grade, email="", subject=""):
        """Add a new student to the list.

        Creates a Student object and appends it to the internal list.

        Args:
            name (str): Full name of the student. Must be non-empty.
            grade (int or float): Numerical grade between 0 and 100.
            email (str): Email address. Defaults to empty string.
            subject (str): Subject/course name. Defaults to empty string.

        Returns:
            Student: The newly created Student object.

        Raises:
            ValueError: If name is empty or grade is out of range.
        """
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        if grade < 0 or grade > 100:
            raise ValueError("Grade must be between 0 and 100")

        student = Student(
            name=name.strip(),
            grade=grade,
            email=email,
            subject=subject
        )
        self._students.append(student)
        return student

    def remove_student(self, index):
        """Remove a student at the given index.

        Args:
            index (int): Zero-based index of the student to remove.

        Returns:
            Student: The removed Student object.

        Raises:
            IndexError: If index is out of range (negative or >= list size).
        """
        if index < 0 or index >= len(self._students):
            raise IndexError("Invalid index")
        return self._students.pop(index)

    def update_student(self, index, name=None, grade=None, email=None, subject=None):
        """Update a student's data at the given index.

        Only the provided fields (non-None) are updated. Unchanged fields
        retain their previous values.

        Args:
            index (int): Zero-based index of the student to update.
            name (str or None): New name, or None to keep current.
            grade (int or float or None): New grade, or None to keep current.
            email (str or None): New email, or None to keep current.
            subject (str or None): New subject, or None to keep current.

        Returns:
            Student: The updated Student object.

        Raises:
            IndexError: If index is out of range.
        """
        if index < 0 or index >= len(self._students):
            raise IndexError("Invalid index")

        student = self._students[index]
        if name is not None:
            student.name = name
        if grade is not None:
            student.grade = grade
        if email is not None:
            student.email = email
        if subject is not None:
            student.subject = subject
        return student

    def get_student(self, index):
        """Get a student at the given index without removing.

        Args:
            index (int): Zero-based index of the student.

        Returns:
            Student: The Student object at the given index.

        Raises:
            IndexError: If index is out of range.
        """
        if index < 0 or index >= len(self._students):
            raise IndexError("Invalid index")
        return self._students[index]

    def get_all_students(self):
        """Get a copy of all students in the list.

        Returns a shallow copy to prevent external modification
        of the internal list.

        Returns:
            list: Copy of all Student objects in the list.
        """
        return self._students.copy()

    def search_by_name(self, name):
        """Search for students whose names contain the given substring.

        Case-insensitive partial match search.

        Args:
            name (str): Substring to search for in student names.

        Returns:
            list: List of tuples (index, Student) for matching students.
                Example: [(0, Student(...)), (2, Student(...))]
        """
        results = []
        for i, student in enumerate(self._students):
            if name.lower() in student.name.lower():
                results.append((i, student))
        return results

    def size(self):
        """Get the number of students in the list.

        Returns:
            int: Total count of students.
        """
        return len(self._students)

    def sort_by_grade(self, ascending=True):
        """Sort the internal list by grade.

        Sorts in-place using Python's Timsort algorithm.

        Args:
            ascending (bool): If True, sort lowest to highest.
                If False, sort highest to lowest. Defaults to True.

        Returns:
            None
        """
        self._students.sort(
            key=lambda s: s.grade,
            reverse=not ascending
        )

    def sort_by_name(self, ascending=True):
        """Sort the internal list alphabetically by name.

        Sorts in-place, case-insensitive.

        Args:
            ascending (bool): If True, A-Z. If False, Z-A. Defaults to True.

        Returns:
            None
        """
        self._students.sort(
            key=lambda s: s.name.lower(),
            reverse=not ascending
        )

    def get_average(self):
        """Calculate the average grade of all students.

        Returns:
            float: Average grade, or 0 if the list is empty.
        """
        if not self._students:
            return 0
        total = sum(s.grade for s in self._students)
        return total / len(self._students)

    def get_highest_grade(self):
        """Get the highest grade among all students.

        Returns:
            float: Maximum grade, or 0 if the list is empty.
        """
        if not self._students:
            return 0
        return max(s.grade for s in self._students)

    def get_lowest_grade(self):
        """Get the lowest grade among all students.

        Returns:
            float: Minimum grade, or 0 if the list is empty.
        """
        if not self._students:
            return 0
        return min(s.grade for s in self._students)

    def get_passing_students(self):
        """Get all students with a passing grade (>= 60).

        Returns:
            list: List of Student objects who are passing.
        """
        return [s for s in self._students if s.is_passing()]

    def get_failing_students(self):
        """Get all students with a failing grade (< 60).

        Returns:
            list: List of Student objects who are failing.
        """
        return [s for s in self._students if not s.is_passing()]

    def get_statistics(self):
        """Get comprehensive statistics for all students.

        Returns a dictionary with total count, average, highest, lowest,
        passing count, and failing count.

        Returns:
            dict: Dictionary with keys:
                - 'total' (int): Number of students.
                - 'average' (float): Average grade.
                - 'highest' (float): Highest grade.
                - 'lowest' (float): Lowest grade.
                - 'passing' (int): Count of passing students.
                - 'failing' (int): Count of failing students.
        """
        if not self._students:
            return {
                "total": 0,
                "average": 0,
                "highest": 0,
                "lowest": 0,
                "passing": 0,
                "failing": 0
            }
        return {
            "total": len(self._students),
            "average": self.get_average(),
            "highest": self.get_highest_grade(),
            "lowest": self.get_lowest_grade(),
            "passing": len(self.get_passing_students()),
            "failing": len(self.get_failing_students())
        }

    def to_list(self):
        """Convert all students to a list of dictionaries.

        Used for JSON serialization and API responses.

        Returns:
            list: List of dictionaries, each representing a student.
        """
        return [s.to_dict() for s in self._students]
