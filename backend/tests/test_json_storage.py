import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
import json
from database.json_storage import JSONStorage
from models.student import Student


class TestJSONStorage(unittest.TestCase):

    def setUp(self):
        self.test_file = os.path.join(os.path.dirname(__file__), "..", "data", "test_storage.json")
        self.storage = JSONStorage(filepath=self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def _create_student(self, name="Ali", grade=92, email="ali@test.com", subject="Math"):
        return Student(name=name, grade=grade, email=email, subject=subject)

    # --- Init ---
    def test_init_creates_empty(self):
        self.assertEqual(self.storage.size(), 0)

    def test_init_creates_directory(self):
        test_dir = os.path.join(os.path.dirname(__file__), "..", "data", "subdir", "test.json")
        s = JSONStorage(filepath=test_dir)
        self.assertTrue(os.path.exists(os.path.dirname(test_dir)))
        if os.path.exists(test_dir):
            os.remove(test_dir)
        subdir = os.path.join(os.path.dirname(__file__), "..", "data", "subdir")
        if os.path.exists(subdir):
            os.rmdir(subdir)

    # --- Add ---
    def test_add_student(self):
        student = self._create_student()
        result = self.storage.add(student)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.name, "Ali")

    def test_add_multiple_students(self):
        self.storage.add(self._create_student("Ali", 92))
        self.storage.add(self._create_student("Sara", 88))
        self.assertEqual(self.storage.size(), 2)

    def test_add_assigns_sequential_ids(self):
        s1 = self.storage.add(self._create_student("Ali", 92))
        s2 = self.storage.add(self._create_student("Sara", 88))
        self.assertEqual(s1.id, 1)
        self.assertEqual(s2.id, 2)

    def test_add_saves_to_file(self):
        self.storage.add(self._create_student())
        self.assertTrue(os.path.exists(self.test_file))
        with open(self.test_file, "r") as f:
            data = json.load(f)
        self.assertEqual(len(data["students"]), 1)

    # --- Get ---
    def test_get_all(self):
        self.storage.add(self._create_student("Ali", 92))
        self.storage.add(self._create_student("Sara", 88))
        students = self.storage.get_all()
        self.assertEqual(len(students), 2)

    def test_get_all_returns_copy(self):
        self.storage.add(self._create_student())
        students = self.storage.get_all()
        students.pop()
        self.assertEqual(self.storage.size(), 1)

    def test_get_by_id_found(self):
        self.storage.add(self._create_student("Ali", 92))
        student = self.storage.get_by_id(1)
        self.assertIsNotNone(student)
        self.assertEqual(student.name, "Ali")

    def test_get_by_id_not_found(self):
        student = self.storage.get_by_id(999)
        self.assertIsNone(student)

    # --- Update ---
    def test_update_student(self):
        student = self.storage.add(self._create_student("Ali", 92))
        student.grade = 95
        result = self.storage.update(student)
        self.assertTrue(result)
        updated = self.storage.get_by_id(student.id)
        self.assertEqual(updated.grade, 95.0)

    def test_update_not_found(self):
        student = self._create_student("Ali", 92)
        student.id = 999
        result = self.storage.update(student)
        self.assertFalse(result)

    # --- Delete ---
    def test_delete_student(self):
        self.storage.add(self._create_student("Ali", 92))
        removed = self.storage.delete(1)
        self.assertIsNotNone(removed)
        self.assertEqual(removed.name, "Ali")
        self.assertEqual(self.storage.size(), 0)

    def test_delete_not_found(self):
        removed = self.storage.delete(999)
        self.assertIsNone(removed)

    def test_delete_saves_to_file(self):
        self.storage.add(self._create_student())
        self.storage.delete(1)
        with open(self.test_file, "r") as f:
            data = json.load(f)
        self.assertEqual(len(data["students"]), 0)

    # --- Search ---
    def test_search_found(self):
        self.storage.add(self._create_student("Ali", 92))
        self.storage.add(self._create_student("Sara", 88))
        results = self.storage.search("Ali")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Ali")

    def test_search_partial(self):
        self.storage.add(self._create_student("Ali", 92))
        self.storage.add(self._create_student("Ahmed", 75))
        results = self.storage.search("a")
        self.assertEqual(len(results), 2)

    def test_search_not_found(self):
        self.storage.add(self._create_student("Ali", 92))
        results = self.storage.search("Zoe")
        self.assertEqual(len(results), 0)

    def test_search_case_insensitive(self):
        self.storage.add(self._create_student("Ali", 92))
        results = self.storage.search("ali")
        self.assertEqual(len(results), 1)

    # --- Stats ---
    def test_stats_empty(self):
        stats = self.storage.get_stats()
        self.assertEqual(stats["total_students"], 0)
        self.assertEqual(stats["average_grade"], 0)

    def test_stats_with_data(self):
        self.storage.add(self._create_student("Ali", 90))
        self.storage.add(self._create_student("Sara", 80))
        stats = self.storage.get_stats()
        self.assertEqual(stats["total_students"], 2)
        self.assertEqual(stats["average_grade"], 85.0)
        self.assertEqual(stats["highest_grade"], 90.0)
        self.assertEqual(stats["lowest_grade"], 80.0)

    def test_stats_grade_distribution(self):
        self.storage.add(self._create_student("Ali", 95))
        self.storage.add(self._create_student("Sara", 85))
        self.storage.add(self._create_student("Ahmed", 75))
        self.storage.add(self._create_student("Hassan", 65))
        self.storage.add(self._create_student("Zoe", 50))
        stats = self.storage.get_stats()
        self.assertEqual(stats["grade_a"], 1)
        self.assertEqual(stats["grade_b"], 1)
        self.assertEqual(stats["grade_c"], 1)
        self.assertEqual(stats["grade_d"], 1)
        self.assertEqual(stats["grade_f"], 1)

    def test_stats_passing_failing(self):
        self.storage.add(self._create_student("Ali", 90))
        self.storage.add(self._create_student("Sara", 50))
        stats = self.storage.get_stats()
        self.assertEqual(stats["passing"], 1)
        self.assertEqual(stats["failing"], 1)

    # --- Size ---
    def test_size_empty(self):
        self.assertEqual(self.storage.size(), 0)

    def test_size_after_add(self):
        self.storage.add(self._create_student())
        self.assertEqual(self.storage.size(), 1)

    # --- Clear ---
    def test_clear(self):
        self.storage.add(self._create_student("Ali", 92))
        self.storage.add(self._create_student("Sara", 88))
        self.storage.clear()
        self.assertEqual(self.storage.size(), 0)

    # --- Save/Load ---
    def test_save_and_load(self):
        self.storage.add(self._create_student("Ali", 92))
        self.storage.add(self._create_student("Sara", 88))

        new_storage = JSONStorage(filepath=self.test_file)
        self.assertEqual(new_storage.size(), 2)
        student = new_storage.get_by_id(1)
        self.assertEqual(student.name, "Ali")

    def test_load_corrupted_file(self):
        with open(self.test_file, "w") as f:
            f.write("not valid json {{{")
        storage = JSONStorage(filepath=self.test_file)
        self.assertEqual(storage.size(), 0)

    def test_load_missing_file(self):
        os.remove(self.test_file) if os.path.exists(self.test_file) else None
        storage = JSONStorage(filepath=self.test_file)
        self.assertEqual(storage.size(), 0)

    # --- get_by_index ---
    def test_get_by_index_first(self):
        self.storage.add(self._create_student("Ali", 92))
        self.storage.add(self._create_student("Sara", 88))
        student = self.storage.get_by_index(0)
        self.assertEqual(student.name, "Ali")

    def test_get_by_index_second(self):
        self.storage.add(self._create_student("Ali", 92))
        self.storage.add(self._create_student("Sara", 88))
        student = self.storage.get_by_index(1)
        self.assertEqual(student.name, "Sara")

    def test_get_by_index_out_of_range(self):
        self.storage.add(self._create_student("Ali", 92))
        student = self.storage.get_by_index(5)
        self.assertIsNone(student)

    def test_get_by_index_negative(self):
        student = self.storage.get_by_index(-1)
        self.assertIsNone(student)

    # --- delete_by_index ---
    def test_delete_by_index(self):
        self.storage.add(self._create_student("Ali", 92))
        self.storage.add(self._create_student("Sara", 88))
        removed = self.storage.delete_by_index(0)
        self.assertEqual(removed.name, "Ali")
        self.assertEqual(self.storage.size(), 1)

    def test_delete_by_index_out_of_range(self):
        removed = self.storage.delete_by_index(5)
        self.assertIsNone(removed)

    # --- sort_by_grade ---
    def test_sort_by_grade_ascending(self):
        self.storage.add(self._create_student("Ali", 92))
        self.storage.add(self._create_student("Sara", 88))
        self.storage.add(self._create_student("Ahmed", 75))
        students = self.storage.sort_by_grade(ascending=True)
        self.assertEqual(students[0].grade, 75.0)
        self.assertEqual(students[1].grade, 88.0)
        self.assertEqual(students[2].grade, 92.0)

    def test_sort_by_grade_descending(self):
        self.storage.add(self._create_student("Ali", 92))
        self.storage.add(self._create_student("Sara", 88))
        students = self.storage.sort_by_grade(ascending=False)
        self.assertEqual(students[0].grade, 92.0)
        self.assertEqual(students[1].grade, 88.0)

    def test_sort_empty(self):
        students = self.storage.sort_by_grade(ascending=True)
        self.assertEqual(len(students), 0)


if __name__ == "__main__":
    unittest.main()
