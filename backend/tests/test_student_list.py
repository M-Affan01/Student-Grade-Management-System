import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from models.student_list import StudentList


class TestStudentList(unittest.TestCase):

    def setUp(self):
        self.sl = StudentList()

    def test_empty_list(self):
        self.assertEqual(self.sl.size(), 0)
        self.assertEqual(self.sl.get_all_students(), [])

    def test_add_student(self):
        s = self.sl.add_student("Ali", 92)
        self.assertEqual(self.sl.size(), 1)
        self.assertEqual(s.name, "Ali")
        self.assertEqual(s.grade, 92.0)

    def test_add_student_with_email_subject(self):
        s = self.sl.add_student("Sara", 88, "sara@test.com", "Science")
        self.assertEqual(s.email, "sara@test.com")
        self.assertEqual(s.subject, "Science")

    def test_add_multiple_students(self):
        self.sl.add_student("Ali", 92)
        self.sl.add_student("Sara", 88)
        self.sl.add_student("Ahmed", 75)
        self.assertEqual(self.sl.size(), 3)

    def test_add_student_empty_name_raises(self):
        with self.assertRaises(ValueError):
            self.sl.add_student("", 92)

    def test_add_student_whitespace_name_raises(self):
        with self.assertRaises(ValueError):
            self.sl.add_student("   ", 92)

    def test_add_student_grade_negative_raises(self):
        with self.assertRaises(ValueError):
            self.sl.add_student("Ali", -1)

    def test_add_student_grade_over_100_raises(self):
        with self.assertRaises(ValueError):
            self.sl.add_student("Ali", 101)

    def test_remove_student(self):
        self.sl.add_student("Ali", 92)
        self.sl.add_student("Sara", 88)
        removed = self.sl.remove_student(0)
        self.assertEqual(removed.name, "Ali")
        self.assertEqual(self.sl.size(), 1)

    def test_remove_student_invalid_index_raises(self):
        self.sl.add_student("Ali", 92)
        with self.assertRaises(IndexError):
            self.sl.remove_student(5)

    def test_remove_student_negative_index_raises(self):
        self.sl.add_student("Ali", 92)
        with self.assertRaises(IndexError):
            self.sl.remove_student(-1)

    def test_update_student(self):
        self.sl.add_student("Ali", 92)
        updated = self.sl.update_student(0, grade=95)
        self.assertEqual(updated.grade, 95.0)

    def test_update_student_name(self):
        self.sl.add_student("Ali", 92)
        updated = self.sl.update_student(0, name="Ahmed")
        self.assertEqual(updated.name, "Ahmed")

    def test_update_student_invalid_index_raises(self):
        with self.assertRaises(IndexError):
            self.sl.update_student(0, grade=95)

    def test_update_student_invalid_grade_raises(self):
        self.sl.add_student("Ali", 92)
        with self.assertRaises(ValueError):
            self.sl.update_student(0, grade=150)

    def test_get_student(self):
        self.sl.add_student("Ali", 92)
        s = self.sl.get_student(0)
        self.assertEqual(s.name, "Ali")

    def test_get_student_invalid_index_raises(self):
        with self.assertRaises(IndexError):
            self.sl.get_student(0)

    def test_get_all_students_returns_copy(self):
        self.sl.add_student("Ali", 92)
        all_students = self.sl.get_all_students()
        all_students.pop()
        self.assertEqual(self.sl.size(), 1)

    def test_search_by_name_exact(self):
        self.sl.add_student("Ali", 92)
        self.sl.add_student("Sara", 88)
        results = self.sl.search_by_name("Ali")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1].name, "Ali")

    def test_search_by_name_partial(self):
        self.sl.add_student("Ali", 92)
        self.sl.add_student("Ahmed", 75)
        self.sl.add_student("Sara", 88)
        results = self.sl.search_by_name("a")
        self.assertEqual(len(results), 3)

    def test_search_by_name_case_insensitive(self):
        self.sl.add_student("Ali", 92)
        results = self.sl.search_by_name("ali")
        self.assertEqual(len(results), 1)

    def test_search_by_name_not_found(self):
        self.sl.add_student("Ali", 92)
        results = self.sl.search_by_name("Zoe")
        self.assertEqual(len(results), 0)

    def test_sort_by_grade_ascending(self):
        self.sl.add_student("Ali", 92)
        self.sl.add_student("Sara", 88)
        self.sl.add_student("Ahmed", 75)
        self.sl.sort_by_grade(ascending=True)
        students = self.sl.get_all_students()
        self.assertEqual(students[0].grade, 75.0)
        self.assertEqual(students[1].grade, 88.0)
        self.assertEqual(students[2].grade, 92.0)

    def test_sort_by_grade_descending(self):
        self.sl.add_student("Ali", 92)
        self.sl.add_student("Sara", 88)
        self.sl.add_student("Ahmed", 75)
        self.sl.sort_by_grade(ascending=False)
        students = self.sl.get_all_students()
        self.assertEqual(students[0].grade, 92.0)
        self.assertEqual(students[1].grade, 88.0)
        self.assertEqual(students[2].grade, 75.0)

    def test_sort_by_name_ascending(self):
        self.sl.add_student("Sara", 88)
        self.sl.add_student("Ali", 92)
        self.sl.add_student("Ahmed", 75)
        self.sl.sort_by_name(ascending=True)
        students = self.sl.get_all_students()
        self.assertEqual(students[0].name, "Ahmed")
        self.assertEqual(students[1].name, "Ali")
        self.assertEqual(students[2].name, "Sara")

    def test_get_average(self):
        self.sl.add_student("Ali", 90)
        self.sl.add_student("Sara", 80)
        avg = self.sl.get_average()
        self.assertEqual(avg, 85.0)

    def test_get_average_empty(self):
        self.assertEqual(self.sl.get_average(), 0)

    def test_get_highest_grade(self):
        self.sl.add_student("Ali", 92)
        self.sl.add_student("Sara", 88)
        self.assertEqual(self.sl.get_highest_grade(), 92.0)

    def test_get_highest_grade_empty(self):
        self.assertEqual(self.sl.get_highest_grade(), 0)

    def test_get_lowest_grade(self):
        self.sl.add_student("Ali", 92)
        self.sl.add_student("Sara", 88)
        self.assertEqual(self.sl.get_lowest_grade(), 88.0)

    def test_get_lowest_grade_empty(self):
        self.assertEqual(self.sl.get_lowest_grade(), 0)

    def test_get_passing_students(self):
        self.sl.add_student("Ali", 92)
        self.sl.add_student("Sara", 55)
        passing = self.sl.get_passing_students()
        self.assertEqual(len(passing), 1)
        self.assertEqual(passing[0].name, "Ali")

    def test_get_failing_students(self):
        self.sl.add_student("Ali", 92)
        self.sl.add_student("Sara", 55)
        failing = self.sl.get_failing_students()
        self.assertEqual(len(failing), 1)
        self.assertEqual(failing[0].name, "Sara")

    def test_get_statistics(self):
        self.sl.add_student("Ali", 92)
        self.sl.add_student("Sara", 88)
        stats = self.sl.get_statistics()
        self.assertEqual(stats["total"], 2)
        self.assertEqual(stats["average"], 90.0)
        self.assertEqual(stats["highest"], 92.0)
        self.assertEqual(stats["lowest"], 88.0)
        self.assertEqual(stats["passing"], 2)
        self.assertEqual(stats["failing"], 0)

    def test_get_statistics_empty(self):
        stats = self.sl.get_statistics()
        self.assertEqual(stats["total"], 0)

    def test_to_list(self):
        self.sl.add_student("Ali", 92)
        self.sl.add_student("Sara", 88)
        result = self.sl.to_list()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Ali")
        self.assertEqual(result[1]["name"], "Sara")

    def test_size(self):
        self.assertEqual(self.sl.size(), 0)
        self.sl.add_student("Ali", 92)
        self.assertEqual(self.sl.size(), 1)
        self.sl.add_student("Sara", 88)
        self.assertEqual(self.sl.size(), 2)


if __name__ == "__main__":
    unittest.main()
