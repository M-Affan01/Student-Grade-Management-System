"""
MySQL Database Storage Module
==============================
Provides persistent data storage using MySQL (XAMPP). Implements the
same storage interface as JSONStorage for seamless backend switching.

Creates a fresh connection per query to avoid stale connections in
background Flask mode. Includes connection pooling for performance.


class MySQLStorage:
    MySQL-based storage backend using mysql-connector-python.
    Creates fresh connections per query to prevent stale connections.
"""


import mysql.connector
from mysql.connector import Error
from models.student import Student


class MySQLStorage:
    """MySQL database storage for Student objects.

    Provides CRUD operations with automatic table creation on init.
    Uses a fresh connection per query to avoid stale connection issues
    when Flask runs in background mode.

    Attributes:
        config (dict): MySQL connection configuration parameters.
    """

    def __init__(self, host="localhost", user="root", password="", database="student_grade_db", port=3306):
        """Initialize MySQL storage and create tables if needed.

        Args:
            host (str): MySQL server hostname. Defaults to 'localhost'.
            user (str): MySQL username. Defaults to 'root'.
            password (str): MySQL password. Defaults to empty string.
            database (str): Database name. Defaults to 'student_grade_db'.
            port (int): MySQL server port. Defaults to 3306.

        Returns:
            None
        """
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database,
            "port": port,
            "autocommit": True,
            "connection_timeout": 5,
            "connect_timeout": 5,
            "pool_name": "student_pool",
            "pool_size": 3,
            "pool_reset_session": True,
        }
        self._create_tables()

    def _get_connection(self):
        """Get a new MySQL connection.

        Tries to create a pooled connection first. If pooling fails
        (e.g., pool already exists), falls back to a simple connection.

        Returns:
            mysql.connector.connection: A new database connection.

        Raises:
            mysql.connector.Error: If connection fails after both attempts.
        """
        try:
            return mysql.connector.connect(**self.config)
        except Error:
            self.config.pop("pool_name", None)
            self.config.pop("pool_size", None)
            self.config.pop("pool_reset_session", None)
            return mysql.connector.connect(**self.config)

    def _execute(self, query, params=None, fetch=False):
        """Execute a SQL query with automatic connection management.

        Opens a connection, executes the query, optionally commits,
        and always closes the connection in the finally block.

        Args:
            query (str): SQL query string with optional %s placeholders.
            params (tuple or None): Query parameters. Defaults to None.
            fetch (bool): If True, returns fetched rows (SELECT).
                If False, returns affected row count (INSERT/UPDATE/DELETE).

        Returns:
            list or int or None:
                - list of dicts if fetch=True (SELECT results)
                - int (row count) if fetch=False (INSERT/UPDATE/DELETE)
                - None on error
        """
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())

            if fetch:
                result = cursor.fetchall()
            else:
                conn.commit()
                result = cursor.rowcount

            cursor.close()
            return result
        except Error as e:
            print(f"Query error: {e}")
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            return None
        finally:
            if conn and conn.is_connected():
                conn.close()

    def _create_tables(self):
        """Create the students table if it doesn't exist.

        Table schema:
            - id: INT AUTO_INCREMENT PRIMARY KEY
            - name: VARCHAR(100) NOT NULL
            - grade: DECIMAL(5,2) NOT NULL
            - email: VARCHAR(150)
            - subject: VARCHAR(100)
            - created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            - updated_at: TIMESTAMP AUTO-UPDATE

        Returns:
            None
        """
        query = """
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            grade DECIMAL(5,2) NOT NULL,
            email VARCHAR(150),
            subject VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        self._execute(query)
        print("MySQL tables ready")

    def get_all(self):
        """Get all students ordered by ID.

        Returns:
            list: List of Student objects, ordered by ascending ID.
                Returns empty list if no students found.
        """
        query = "SELECT * FROM students ORDER BY id"
        results = self._execute(query, fetch=True)
        if results:
            return [Student.from_dict(row) for row in results]
        return []

    def get_by_id(self, student_id):
        """Find a student by their unique ID.

        Args:
            student_id (int): The ID to search for.

        Returns:
            Student or None: The matching Student, or None if not found.
        """
        query = "SELECT * FROM students WHERE id = %s"
        results = self._execute(query, (student_id,), fetch=True)
        if results:
            return Student.from_dict(results[0])
        return None

    def add(self, student):
        """Insert a new student and retrieve the auto-generated ID.

        Inserts the student record then queries LAST_INSERT_ID()
        to get the auto-assigned ID.

        Args:
            student (Student): Student to add (ID will be auto-assigned).

        Returns:
            Student or None: The added Student with the new ID, or None on error.
        """
        query = """
        INSERT INTO students (name, grade, email, subject)
        VALUES (%s, %s, %s, %s)
        """
        params = (student.name, student.grade, student.email, student.subject)
        result = self._execute(query, params)
        if result is not None:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT LAST_INSERT_ID()")
            student.id = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return student
        return None

    def update(self, student):
        """Update an existing student's record.

        Args:
            student (Student): Student with updated data (must have valid ID).

        Returns:
            bool: True if a row was updated, False otherwise.
        """
        query = """
        UPDATE students
        SET name = %s, grade = %s, email = %s, subject = %s
        WHERE id = %s
        """
        params = (student.name, student.grade, student.email, student.subject, student.id)
        result = self._execute(query, params)
        return result is not None and result > 0

    def delete(self, student_id):
        """Delete a student by ID.

        First checks if the student exists before attempting deletion.

        Args:
            student_id (int): ID of the student to delete.

        Returns:
            bool: True if deleted, False if not found or error.
        """
        student = self.get_by_id(student_id)
        if student:
            query = "DELETE FROM students WHERE id = %s"
            result = self._execute(query, (student_id,))
            return result is not None and result > 0
        return False

    def search(self, name):
        """Search for students by name (case-insensitive LIKE query).

        Args:
            name (str): Substring to search for in student names.

        Returns:
            list: List of matching Student objects.
        """
        query = "SELECT * FROM students WHERE name LIKE %s ORDER BY id"
        results = self._execute(query, (f"%{name}%",), fetch=True)
        if results:
            return [Student.from_dict(row) for row in results]
        return []

    def get_stats(self):
        """Calculate comprehensive statistics using SQL aggregation.

        Uses a single SQL query with SUM/CASE statements for efficient
        grade distribution calculation on the database server.

        Returns:
            dict: Statistics with keys:
                total_students, average_grade, highest_grade, lowest_grade,
                passing, failing, grade_a, grade_b, grade_c, grade_d, grade_f
        """
        query = """
        SELECT
            COUNT(*) as total_students,
            COALESCE(AVG(grade), 0) as average_grade,
            COALESCE(MAX(grade), 0) as highest_grade,
            COALESCE(MIN(grade), 0) as lowest_grade,
            SUM(CASE WHEN grade >= 60 THEN 1 ELSE 0 END) as passing,
            SUM(CASE WHEN grade < 60 THEN 1 ELSE 0 END) as failing,
            SUM(CASE WHEN grade >= 90 THEN 1 ELSE 0 END) as grade_a,
            SUM(CASE WHEN grade >= 80 AND grade < 90 THEN 1 ELSE 0 END) as grade_b,
            SUM(CASE WHEN grade >= 70 AND grade < 80 THEN 1 ELSE 0 END) as grade_c,
            SUM(CASE WHEN grade >= 60 AND grade < 70 THEN 1 ELSE 0 END) as grade_d,
            SUM(CASE WHEN grade < 60 THEN 1 ELSE 0 END) as grade_f
        FROM students
        """
        results = self._execute(query, fetch=True)
        if results and results[0]:
            s = results[0]
            return {
                "total_students": int(s["total_students"] or 0),
                "average_grade": round(float(s["average_grade"] or 0), 2),
                "highest_grade": float(s["highest_grade"] or 0),
                "lowest_grade": float(s["lowest_grade"] or 0),
                "passing": int(s["passing"] or 0),
                "failing": int(s["failing"] or 0),
                "grade_a": int(s["grade_a"] or 0),
                "grade_b": int(s["grade_b"] or 0),
                "grade_c": int(s["grade_c"] or 0),
                "grade_d": int(s["grade_d"] or 0),
                "grade_f": int(s["grade_f"] or 0)
            }
        return {
            "total_students": 0, "average_grade": 0, "highest_grade": 0,
            "lowest_grade": 0, "passing": 0, "failing": 0,
            "grade_a": 0, "grade_b": 0, "grade_c": 0, "grade_d": 0, "grade_f": 0
        }

    def get_by_index(self, index):
        """Get a student by their list position (0-based, ordered by ID).

        Uses SQL OFFSET to efficiently retrieve the nth student.

        Args:
            index (int): Zero-based position.

        Returns:
            Student or None: The Student at that position, or None if out of range.
        """
        query = "SELECT * FROM students ORDER BY id LIMIT 1 OFFSET %s"
        results = self._execute(query, (index,), fetch=True)
        if results:
            return Student.from_dict(results[0])
        return None

    def delete_by_index(self, index):
        """Delete a student by their list position.

        First retrieves the student at the given index, then deletes by ID.

        Args:
            index (int): Zero-based position.

        Returns:
            bool: True if deleted, False if index out of range or error.
        """
        students = self.get_all()
        if 0 <= index < len(students):
            student = students[index]
            return self.delete(student.id)
        return None

    def sort_by_grade(self, ascending=True):
        """Get all students sorted by grade.

        Args:
            ascending (bool): True for lowest-to-highest, False for
                highest-to-lowest. Defaults to True.

        Returns:
            list: List of Student objects sorted by grade.
        """
        order = "ASC" if ascending else "DESC"
        query = f"SELECT * FROM students ORDER BY grade {order}"
        results = self._execute(query, fetch=True)
        if results:
            return [Student.from_dict(row) for row in results]
        return []

    def size(self):
        """Get the total number of students.

        Uses SQL COUNT for efficient counting.

        Returns:
            int: Total number of students in the database.
        """
        query = "SELECT COUNT(*) as count FROM students"
        results = self._execute(query, fetch=True)
        if results:
            return int(results[0]["count"])
        return 0

    def clear(self):
        """Delete all students and reset the auto-increment counter.

        Removes all rows and resets ID sequence to start from 1.

        Returns:
            None
        """
        self._execute("DELETE FROM students")
        self._execute("ALTER TABLE students AUTO_INCREMENT = 1")

    def is_connected(self):
        """Check if MySQL server is reachable.

        Attempts to create and immediately close a connection.

        Returns:
            bool: True if connection succeeded, False otherwise.
        """
        try:
            conn = self._get_connection()
            conn.close()
            return True
        except:
            return False
