"""
JSON File Storage Module
=========================
Provides persistent data storage using JSON files. Implements the storage
interface used by the Flask backend for CRUD operations on student data.

Automatically saves to disk after every write operation and loads
on startup. Maintains a next_id counter for sequential ID assignment.


class JSONStorage:
    File-based storage backend using JSON for persistence.
    Saves data to a local file after every mutation.
"""


import json
import os
from datetime import datetime
from models.student import Student


class JSONStorage:
    """JSON file-based storage for Student objects.

    Provides CRUD operations with automatic file persistence.
    Each write operation triggers an immediate save to disk.
    Data is loaded from the file on initialization.

    Attributes:
        filepath (str): Path to the JSON data file.
        students (list): In-memory list of Student objects.
        next_id (int): Auto-incrementing ID counter for new students.
    """

    def __init__(self, filepath="data/students.json"):
        """Initialize JSONStorage and load existing data.

        Creates the data directory if it doesn't exist, then loads
        any existing students from the JSON file.

        Args:
            filepath (str): Path to the JSON storage file.
                Defaults to 'data/students.json'.

        Returns:
            None
        """
        self.filepath = filepath
        self.students = []
        self.next_id = 1
        self._ensure_directory()
        self.load()

    def _ensure_directory(self):
        """Create the data directory if it doesn't exist.

        Extracts the directory path from self.filepath and creates
        it recursively if missing.

        Returns:
            None
        """
        directory = os.path.dirname(self.filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def load(self):
        """Load student data from the JSON file.

        Reads the file and reconstructs Student objects. If the file
        doesn't exist or is corrupted, initializes with empty data.

        File format:
            {
                "metadata": {...},
                "next_id": 5,
                "students": [{...}, {...}]
            }

        Returns:
            None
        """
        if not os.path.exists(self.filepath):
            self.students = []
            self.next_id = 1
            return

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.students = []
                for item in data.get("students", []):
                    student = Student(
                        student_id=item["id"],
                        name=item["name"],
                        grade=item["grade"],
                        email=item.get("email", ""),
                        subject=item.get("subject", "")
                    )
                    self.students.append(student)

                self.next_id = data.get("next_id", len(self.students) + 1)
                print(f"Loaded {len(self.students)} students from {self.filepath}")
        except json.JSONDecodeError as e:
            print(f"Error reading JSON file: {e}")
            self.students = []
            self.next_id = 1
        except Exception as e:
            print(f"Error loading students: {e}")
            self.students = []
            self.next_id = 1

    def save(self):
        """Persist current student data to the JSON file.

        Writes all students, metadata (count, timestamp, version),
        and the next_id counter to the file in pretty-printed JSON.

        Returns:
            bool: True if save was successful, False on error.
        """
        try:
            data = {
                "metadata": {
                    "total_students": len(self.students),
                    "last_saved": datetime.now().isoformat(),
                    "version": "1.0"
                },
                "next_id": self.next_id,
                "students": [s.to_dict() for s in self.students]
            }

            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"Saved {len(self.students)} students to {self.filepath}")
            return True
        except Exception as e:
            print(f"Error saving students: {e}")
            return False

    def get_all(self):
        """Get a copy of all students.

        Returns:
            list: Copy of all Student objects in storage.
        """
        return self.students.copy()

    def get_by_id(self, student_id):
        """Find a student by their unique ID.

        Args:
            student_id (int): The unique identifier to search for.

        Returns:
            Student or None: The matching Student, or None if not found.
        """
        for s in self.students:
            if s.id == student_id:
                return s
        return None

    def add(self, student):
        """Add a new student and save to disk.

        Assigns the next sequential ID to the student, appends to
        the list, and saves immediately.

        Args:
            student (Student): Student object to add (ID will be overwritten).

        Returns:
            Student: The added Student with the new ID assigned.
        """
        student.id = self.next_id
        self.next_id += 1
        self.students.append(student)
        self.save()
        return student

    def update(self, student):
        """Update an existing student's data and save to disk.

        Finds the student by ID and replaces it in the list.

        Args:
            student (Student): Student object with the updated data.
                Must have a valid 'id' matching an existing student.

        Returns:
            bool: True if student was found and updated, False otherwise.
        """
        for i, s in enumerate(self.students):
            if s.id == student.id:
                self.students[i] = student
                self.save()
                return True
        return False

    def delete(self, student_id):
        """Delete a student by ID and save to disk.

        Args:
            student_id (int): ID of the student to delete.

        Returns:
            Student or None: The deleted Student object, or None if not found.
        """
        for i, s in enumerate(self.students):
            if s.id == student_id:
                removed = self.students.pop(i)
                self.save()
                return removed
        return None

    def search(self, name):
        """Search for students by name (case-insensitive partial match).

        Args:
            name (str): Substring to search for in student names.

        Returns:
            list: List of Student objects whose names contain the query.
        """
        return [s for s in self.students if name.lower() in s.name.lower()]

    def get_stats(self):
        """Calculate comprehensive statistics for all students.

        Computes total count, average, highest, lowest, passing/failing
        counts, and grade distribution (A/B/C/D/F).

        Returns:
            dict: Statistics dictionary with keys:
                - total_students (int), average_grade (float)
                - highest_grade (float), lowest_grade (float)
                - passing (int), failing (int)
                - grade_a (int), grade_b (int), grade_c (int)
                - grade_d (int), grade_f (int)
        """
        if not self.students:
            return {
                "total_students": 0,
                "average_grade": 0,
                "highest_grade": 0,
                "lowest_grade": 0,
                "passing": 0,
                "failing": 0,
                "grade_a": 0,
                "grade_b": 0,
                "grade_c": 0,
                "grade_d": 0,
                "grade_f": 0
            }

        grades = [s.grade for s in self.students]
        grade_a = sum(1 for g in grades if g >= 90)
        grade_b = sum(1 for g in grades if 80 <= g < 90)
        grade_c = sum(1 for g in grades if 70 <= g < 80)
        grade_d = sum(1 for g in grades if 60 <= g < 70)
        grade_f = sum(1 for g in grades if g < 60)
        passing = sum(1 for g in grades if g >= 60)

        return {
            "total_students": len(self.students),
            "average_grade": round(sum(grades) / len(grades), 2),
            "highest_grade": max(grades),
            "lowest_grade": min(grades),
            "passing": passing,
            "failing": len(self.students) - passing,
            "grade_a": grade_a,
            "grade_b": grade_b,
            "grade_c": grade_c,
            "grade_d": grade_d,
            "grade_f": grade_f
        }

    def get_by_index(self, index):
        """Get a student by their list index (0-based).

        Args:
            index (int): Zero-based position in the list.

        Returns:
            Student or None: The Student at that index, or None if out of range.
        """
        if 0 <= index < len(self.students):
            return self.students[index]
        return None

    def delete_by_index(self, index):
        """Delete a student by their list index and save to disk.

        Args:
            index (int): Zero-based position in the list.

        Returns:
            Student or None: The deleted Student, or None if out of range.
        """
        if 0 <= index < len(self.students):
            removed = self.students.pop(index)
            self.save()
            return removed
        return None

    def sort_by_grade(self, ascending=True):
        """Sort students by grade and return a copy.

        Args:
            ascending (bool): True for lowest-to-highest, False for
                highest-to-lowest. Defaults to True.

        Returns:
            list: Copy of all students sorted by grade.
        """
        self.students.sort(key=lambda s: s.grade, reverse=not ascending)
        return self.get_all()

    def size(self):
        """Get the total number of students in storage.

        Returns:
            int: Number of students.
        """
        return len(self.students)

    def clear(self):
        """Remove all students and reset the ID counter.

        Deletes all data and saves the empty state to disk.

        Returns:
            None
        """
        self.students = []
        self.next_id = 1
        self.save()
