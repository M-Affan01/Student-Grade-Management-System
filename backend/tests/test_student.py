import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from models.student import Student


class TestStudent(unittest.TestCase):

    def setUp(self):
        self.student = Student(student_id=1, name="Ali", grade=92.0, email="ali@test.com", subject="Math")

    def test_create_student(self):
        self.assertEqual(self.student.id, 1)
        self.assertEqual(self.student.name, "Ali")
        self.assertEqual(self.student.grade, 92.0)
        self.assertEqual(self.student.email, "ali@test.com")
        self.assertEqual(self.student.subject, "Math")

    def test_create_student_defaults(self):
        s = Student()
        self.assertIsNone(s.id)
        self.assertEqual(s.name, "")
        self.assertEqual(s.grade, 0)
        self.assertEqual(s.email, "")
        self.assertEqual(s.subject, "")

    def test_set_name(self):
        self.student.name = "Sara"
        self.assertEqual(self.student.name, "Sara")

    def test_set_name_strips_whitespace(self):
        self.student.name = "  Ahmed  "
        self.assertEqual(self.student.name, "Ahmed")

    def test_set_grade_valid(self):
        self.student.grade = 85
        self.assertEqual(self.student.grade, 85.0)

    def test_set_grade_zero(self):
        self.student.grade = 0
        self.assertEqual(self.student.grade, 0.0)

    def test_set_grade_hundred(self):
        self.student.grade = 100
        self.assertEqual(self.student.grade, 100.0)

    def test_set_grade_negative_raises(self):
        with self.assertRaises(ValueError):
            self.student.grade = -1

    def test_set_grade_over_100_raises(self):
        with self.assertRaises(ValueError):
            self.student.grade = 101

    def test_set_grade_non_number_raises(self):
        with self.assertRaises((TypeError, ValueError)):
            self.student.grade = "abc"

    def test_grade_returns_float(self):
        s = Student(grade=85)
        self.assertIsInstance(s.grade, float)

    def test_to_dict(self):
        d = self.student.to_dict()
        self.assertEqual(d["id"], 1)
        self.assertEqual(d["name"], "Ali")
        self.assertEqual(d["grade"], 92.0)
        self.assertEqual(d["email"], "ali@test.com")
        self.assertEqual(d["subject"], "Math")

    def test_from_dict(self):
        data = {"id": 2, "name": "Sara", "grade": 88.0, "email": "sara@test.com", "subject": "Science"}
        s = Student.from_dict(data)
        self.assertEqual(s.id, 2)
        self.assertEqual(s.name, "Sara")
        self.assertEqual(s.grade, 88.0)
        self.assertEqual(s.email, "sara@test.com")
        self.assertEqual(s.subject, "Science")

    def test_from_dict_defaults(self):
        s = Student.from_dict({})
        self.assertIsNone(s.id)
        self.assertEqual(s.name, "")
        self.assertEqual(s.grade, 0)

    def test_get_letter_grade_a(self):
        self.student.grade = 95
        self.assertEqual(self.student.get_letter_grade(), "A")

    def test_get_letter_grade_b(self):
        self.student.grade = 85
        self.assertEqual(self.student.get_letter_grade(), "B")

    def test_get_letter_grade_c(self):
        self.student.grade = 75
        self.assertEqual(self.student.get_letter_grade(), "C")

    def test_get_letter_grade_d(self):
        self.student.grade = 65
        self.assertEqual(self.student.get_letter_grade(), "D")

    def test_get_letter_grade_f(self):
        self.student.grade = 50
        self.assertEqual(self.student.get_letter_grade(), "F")

    def test_is_passing(self):
        self.student.grade = 60
        self.assertTrue(self.student.is_passing())

    def test_is_passing_high(self):
        self.student.grade = 95
        self.assertTrue(self.student.is_passing())

    def test_is_not_passing(self):
        self.student.grade = 59
        self.assertFalse(self.student.is_passing())

    def test_str_representation(self):
        s = str(self.student)
        self.assertIn("Ali", s)
        self.assertIn("92.0", s)

    def test_repr_representation(self):
        r = repr(self.student)
        self.assertIn("Ali", r)


if __name__ == "__main__":
    unittest.main()
