import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from utils.validator import Validator


class TestValidator(unittest.TestCase):

    # --- sanitize_input ---
    def test_sanitize_input_normal(self):
        self.assertEqual(Validator.sanitize_input("Ali"), "Ali")

    def test_sanitize_input_html_escape(self):
        result = Validator.sanitize_input("<script>alert('xss')</script>")
        self.assertNotIn("<script>", result)

    def test_sanitize_input_strips_whitespace(self):
        self.assertEqual(Validator.sanitize_input("  Ali  "), "Ali")

    def test_sanitize_input_non_string(self):
        self.assertEqual(Validator.sanitize_input(123), 123)

    # --- contains_xss ---
    def test_contains_xss_script_tag(self):
        self.assertTrue(Validator.contains_xss("<script>alert(1)</script>"))

    def test_contains_xss_event_handler(self):
        self.assertTrue(Validator.contains_xss("onclick=alert(1)"))

    def test_contains_xss_iframe(self):
        self.assertTrue(Validator.contains_xss("<iframe src='evil.com'>"))

    def test_contains_xss_clean(self):
        self.assertFalse(Validator.contains_xss("Ali Khan"))

    def test_contains_xss_non_string(self):
        self.assertFalse(Validator.contains_xss(123))

    # --- validate_name ---
    def test_validate_name_valid(self):
        valid, msg = Validator.validate_name("Ali")
        self.assertTrue(valid)
        self.assertEqual(msg, "")

    def test_validate_name_with_spaces(self):
        valid, msg = Validator.validate_name("Ali Khan")
        self.assertTrue(valid)

    def test_validate_name_with_hyphen(self):
        valid, msg = Validator.validate_name("Ali-Khan")
        self.assertTrue(valid)

    def test_validate_name_with_apostrophe(self):
        valid, msg = Validator.validate_name("Ali's")
        self.assertTrue(valid)

    def test_validate_name_empty(self):
        valid, msg = Validator.validate_name("")
        self.assertFalse(valid)
        self.assertIn("required", msg)

    def test_validate_name_none(self):
        valid, msg = Validator.validate_name(None)
        self.assertFalse(valid)

    def test_validate_name_too_short(self):
        valid, msg = Validator.validate_name("A")
        self.assertFalse(valid)
        self.assertIn("2 characters", msg)

    def test_validate_name_too_long(self):
        valid, msg = Validator.validate_name("A" * 101)
        self.assertFalse(valid)
        self.assertIn("100 characters", msg)

    def test_validate_name_numbers(self):
        valid, msg = Validator.validate_name("123abc")
        self.assertFalse(valid)
        self.assertIn("letters", msg)

    def test_validate_name_xss(self):
        valid, msg = Validator.validate_name("<script>alert(1)</script>")
        self.assertFalse(valid)

    # --- validate_grade ---
    def test_validate_grade_valid(self):
        valid, msg = Validator.validate_grade(85)
        self.assertTrue(valid)

    def test_validate_grade_zero(self):
        valid, msg = Validator.validate_grade(0)
        self.assertTrue(valid)

    def test_validate_grade_hundred(self):
        valid, msg = Validator.validate_grade(100)
        self.assertTrue(valid)

    def test_validate_grade_float(self):
        valid, msg = Validator.validate_grade(85.5)
        self.assertTrue(valid)

    def test_validate_grade_string_number(self):
        valid, msg = Validator.validate_grade("85")
        self.assertTrue(valid)

    def test_validate_grade_empty(self):
        valid, msg = Validator.validate_grade("")
        self.assertFalse(valid)
        self.assertIn("required", msg)

    def test_validate_grade_none(self):
        valid, msg = Validator.validate_grade(None)
        self.assertFalse(valid)

    def test_validate_grade_negative(self):
        valid, msg = Validator.validate_grade(-1)
        self.assertFalse(valid)
        self.assertIn("negative", msg)

    def test_validate_grade_over_100(self):
        valid, msg = Validator.validate_grade(101)
        self.assertFalse(valid)
        self.assertIn("exceed", msg)

    def test_validate_grade_not_number(self):
        valid, msg = Validator.validate_grade("abc")
        self.assertFalse(valid)
        self.assertIn("valid number", msg)

    # --- validate_email ---
    def test_validate_email_valid(self):
        valid, msg = Validator.validate_email("test@gmail.com")
        self.assertTrue(valid)

    def test_validate_email_empty(self):
        valid, msg = Validator.validate_email("")
        self.assertFalse(valid)
        self.assertIn("required", msg)

    def test_validate_email_none(self):
        valid, msg = Validator.validate_email(None)
        self.assertFalse(valid)
        self.assertIn("required", msg)

    def test_validate_email_invalid_format(self):
        valid, msg = Validator.validate_email("not-an-email")
        self.assertFalse(valid)

    def test_validate_email_no_domain(self):
        valid, msg = Validator.validate_email("test@")
        self.assertFalse(valid)

    def test_validate_email_too_long(self):
        valid, msg = Validator.validate_email("a" * 151)
        self.assertFalse(valid)
        self.assertIn("150 characters", msg)

    # --- validate_subject ---
    def test_validate_subject_valid(self):
        valid, msg = Validator.validate_subject("Math")
        self.assertTrue(valid)

    def test_validate_subject_empty(self):
        valid, msg = Validator.validate_subject("")
        self.assertFalse(valid)
        self.assertIn("required", msg)

    def test_validate_subject_none(self):
        valid, msg = Validator.validate_subject(None)
        self.assertFalse(valid)
        self.assertIn("required", msg)

    def test_validate_subject_with_hyphen(self):
        valid, msg = Validator.validate_subject("Computer-Science")
        self.assertTrue(valid)

    def test_validate_subject_numbers(self):
        valid, msg = Validator.validate_subject("Math123")
        self.assertFalse(valid)
        self.assertIn("letters", msg)

    def test_validate_subject_too_long(self):
        valid, msg = Validator.validate_subject("A" * 101)
        self.assertFalse(valid)

    # --- validate_student_data ---
    def test_validate_student_data_valid(self):
        data = {"name": "Ali", "grade": 92, "email": "ali@gmail.com", "subject": "Math"}
        valid, errors = Validator.validate_student_data(data)
        self.assertTrue(valid)
        self.assertEqual(errors, {})

    def test_validate_student_data_full(self):
        data = {"name": "Ali", "grade": 92, "email": "ali@gmail.com", "subject": "Math"}
        valid, errors = Validator.validate_student_data(data)
        self.assertTrue(valid)

    def test_validate_student_data_empty_name(self):
        data = {"name": "", "grade": 92, "email": "ali@gmail.com", "subject": "Math"}
        valid, errors = Validator.validate_student_data(data)
        self.assertFalse(valid)
        self.assertIn("name", errors)

    def test_validate_student_data_invalid_grade(self):
        data = {"name": "Ali", "grade": 150, "email": "ali@gmail.com", "subject": "Math"}
        valid, errors = Validator.validate_student_data(data)
        self.assertFalse(valid)
        self.assertIn("grade", errors)

    def test_validate_student_data_missing_grade(self):
        data = {"name": "Ali", "email": "ali@gmail.com", "subject": "Math"}
        valid, errors = Validator.validate_student_data(data)
        self.assertFalse(valid)
        self.assertIn("grade", errors)

    def test_validate_student_data_invalid_email(self):
        data = {"name": "Ali", "grade": 92, "email": "bad-email", "subject": "Math"}
        valid, errors = Validator.validate_student_data(data)
        self.assertFalse(valid)
        self.assertIn("email", errors)

    def test_validate_student_data_none(self):
        valid, errors = Validator.validate_student_data(None)
        self.assertFalse(valid)

    def test_validate_student_data_multiple_errors(self):
        data = {"name": "", "grade": -5, "email": "bad"}
        valid, errors = Validator.validate_student_data(data)
        self.assertFalse(valid)
        self.assertTrue(len(errors) >= 2)

    # --- validate_id ---
    def test_validate_id_valid(self):
        valid, msg = Validator.validate_id(1)
        self.assertTrue(valid)

    def test_validate_id_zero(self):
        valid, msg = Validator.validate_id(0)
        self.assertFalse(valid)
        self.assertIn("positive", msg)

    def test_validate_id_negative(self):
        valid, msg = Validator.validate_id(-1)
        self.assertFalse(valid)

    def test_validate_id_none(self):
        valid, msg = Validator.validate_id(None)
        self.assertFalse(valid)

    def test_validate_id_string(self):
        valid, msg = Validator.validate_id("abc")
        self.assertFalse(valid)
        self.assertIn("number", msg)


if __name__ == "__main__":
    unittest.main()
