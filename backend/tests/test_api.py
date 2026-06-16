import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
import json
from app import create_app
from database.storage_factory import create_storage


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.test_storage = create_storage("json", {"filepath": "data/test_students.json"})
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.storage = self.test_storage
        self.test_storage.clear()
        self.client = self.app.test_client()

    def tearDown(self):
        self.test_storage.clear()
        test_file = os.path.join(os.path.dirname(__file__), "..", "data", "test_students.json")
        if os.path.exists(test_file):
            os.remove(test_file)

    def _add_student(self, name="Ali", grade=92, email="ali@gmail.com", subject="Math"):
        return self.client.post(
            "/api/students",
            data=json.dumps({"name": name, "grade": grade, "email": email, "subject": subject}),
            content_type="application/json"
        )

    # --- Health ---
    def test_health(self):
        resp = self.client.get("/api/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["status"], "ok")

    # --- Add Student ---
    def test_add_student_success(self):
        resp = self._add_student()
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertEqual(data["student"]["name"], "Ali")
        self.assertEqual(data["student"]["grade"], 92.0)

    def test_add_student_empty_name(self):
        resp = self._add_student(name="")
        self.assertEqual(resp.status_code, 400)

    def test_add_student_invalid_grade_over(self):
        resp = self._add_student(grade=150)
        self.assertEqual(resp.status_code, 400)

    def test_add_student_invalid_grade_negative(self):
        resp = self._add_student(grade=-5)
        self.assertEqual(resp.status_code, 400)

    def test_add_student_invalid_email(self):
        resp = self._add_student(email="bad-email")
        self.assertEqual(resp.status_code, 400)

    def test_add_student_invalid_json(self):
        resp = self.client.post(
            "/api/students",
            data="not json",
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 400)

    def test_add_student_duplicate_name(self):
        self._add_student(name="Ali")
        resp = self._add_student(name="Ali")
        self.assertEqual(resp.status_code, 409)

    def test_add_student_sanitizes_xss(self):
        resp = self._add_student(name="<script>alert(1)</script>")
        self.assertEqual(resp.status_code, 400)

    # --- Get All Students ---
    def test_get_students_empty(self):
        resp = self.client.get("/api/students")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json(), [])

    def test_get_students_with_data(self):
        self._add_student("Ali", 92)
        self._add_student("Sara", 88)
        resp = self.client.get("/api/students")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(len(data), 2)

    # --- Get Student by ID ---
    def test_get_student_by_id(self):
        self._add_student("Ali", 92)
        resp = self.client.get("/api/students/1")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["name"], "Ali")

    def test_get_student_not_found(self):
        resp = self.client.get("/api/students/999")
        self.assertEqual(resp.status_code, 404)

    # --- Update Student ---
    def test_update_student(self):
        self._add_student("Ali", 92)
        resp = self.client.put(
            "/api/students/1",
            data=json.dumps({"name": "Ali", "grade": 95, "email": "ali@gmail.com", "subject": "Math"}),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["student"]["grade"], 95.0)

    def test_update_student_not_found(self):
        resp = self.client.put(
            "/api/students/999",
            data=json.dumps({"name": "Ali", "grade": 95, "email": "ali@gmail.com", "subject": "Math"}),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 404)

    def test_update_student_invalid_grade(self):
        self._add_student("Ali", 92)
        resp = self.client.put(
            "/api/students/1",
            data=json.dumps({"name": "Ali", "grade": 200, "email": "ali@gmail.com", "subject": "Math"}),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 400)

    def test_update_student_duplicate_name(self):
        self._add_student("Ali", 92)
        self._add_student("Sara", 88)
        resp = self.client.put(
            "/api/students/2",
            data=json.dumps({"name": "Ali", "grade": 88, "email": "sara@gmail.com", "subject": "Science"}),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 409)

    # --- Delete Student ---
    def test_delete_student(self):
        self._add_student("Ali", 92)
        resp = self.client.delete("/api/students/1")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("deleted", resp.get_json()["message"])

    def test_delete_student_not_found(self):
        resp = self.client.delete("/api/students/999")
        self.assertEqual(resp.status_code, 404)

    # --- Search ---
    def test_search_found(self):
        self._add_student("Ali", 92)
        self._add_student("Sara", 88)
        resp = self.client.get("/api/students/search?name=Ali")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["count"], 1)

    def test_search_not_found(self):
        self._add_student("Ali", 92)
        resp = self.client.get("/api/students/search?name=Zoe")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["count"], 0)

    def test_search_partial(self):
        self._add_student("Ali", 92)
        self._add_student("Ahmed", 75)
        resp = self.client.get("/api/students/search?name=a")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["count"], 2)

    # --- Stats ---
    def test_stats_empty(self):
        resp = self.client.get("/api/students/stats")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["total_students"], 0)

    def test_stats_with_data(self):
        self._add_student("Ali", 92)
        self._add_student("Sara", 88)
        resp = self.client.get("/api/students/stats")
        data = resp.get_json()
        self.assertEqual(data["total_students"], 2)
        self.assertEqual(data["average_grade"], 90.0)
        self.assertEqual(data["highest_grade"], 92.0)
        self.assertEqual(data["lowest_grade"], 88.0)

    def test_stats_grade_distribution(self):
        self._add_student("Ali", 95)
        self._add_student("Sara", 85)
        self._add_student("Ahmed", 75)
        self._add_student("Hassan", 55)
        resp = self.client.get("/api/students/stats")
        data = resp.get_json()
        self.assertEqual(data["grade_a"], 1)
        self.assertEqual(data["grade_b"], 1)
        self.assertEqual(data["grade_c"], 1)
        self.assertEqual(data["grade_f"], 1)

    # --- Storage Info ---
    def test_storage_info(self):
        resp = self.client.get("/api/storage/info")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("type", data)
        self.assertIn("students_count", data)

    # --- Storage Save/Load ---
    def test_storage_save(self):
        self._add_student("Ali", 92)
        resp = self.client.post("/api/storage/save")
        self.assertEqual(resp.status_code, 200)

    def test_storage_load(self):
        resp = self.client.post("/api/storage/load")
        self.assertEqual(resp.status_code, 200)

    # --- sortByGrade API ---
    def test_sort_by_grade_ascending(self):
        self._add_student("Ali", 92)
        self._add_student("Sara", 88)
        self._add_student("Ahmed", 75)
        resp = self.client.get("/api/students/sort?ascending=true")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["students"][0]["grade"], 75.0)
        self.assertEqual(data["students"][2]["grade"], 92.0)
        self.assertTrue(data["ascending"])

    def test_sort_by_grade_descending(self):
        self._add_student("Ali", 92)
        self._add_student("Sara", 88)
        resp = self.client.get("/api/students/sort?ascending=false")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["students"][0]["grade"], 92.0)
        self.assertEqual(data["students"][1]["grade"], 88.0)

    def test_sort_empty(self):
        resp = self.client.get("/api/students/sort?ascending=true")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["count"], 0)

    # --- getStudent by index API ---
    def test_get_student_by_index(self):
        self._add_student("Ali", 92)
        self._add_student("Sara", 88)
        resp = self.client.get("/api/students/index/0")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["name"], "Ali")

    def test_get_student_by_index_second(self):
        self._add_student("Ali", 92)
        self._add_student("Sara", 88)
        resp = self.client.get("/api/students/index/1")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["name"], "Sara")

    def test_get_student_by_index_out_of_range(self):
        self._add_student("Ali", 92)
        resp = self.client.get("/api/students/index/5")
        self.assertEqual(resp.status_code, 400)

    def test_get_student_by_index_negative(self):
        resp = self.client.get("/api/students/index/-1")
        self.assertIn(resp.status_code, [400, 404])

    # --- removeStudent by index API ---
    def test_delete_student_by_index(self):
        self._add_student("Ali", 92)
        self._add_student("Sara", 88)
        resp = self.client.delete("/api/students/index/0")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("deleted", resp.get_json()["message"])
        resp = self.client.get("/api/students")
        self.assertEqual(len(resp.get_json()), 1)

    def test_delete_student_by_index_out_of_range(self):
        resp = self.client.delete("/api/students/index/5")
        self.assertEqual(resp.status_code, 400)

    # --- updateGrade by index API ---
    def test_update_grade_by_index(self):
        self._add_student("Ali", 92)
        resp = self.client.put(
            "/api/students/index/0/grade",
            data=json.dumps({"grade": 95}),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["student"]["grade"], 95.0)

    def test_update_grade_by_index_invalid(self):
        self._add_student("Ali", 92)
        resp = self.client.put(
            "/api/students/index/0/grade",
            data=json.dumps({"grade": 200}),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 400)

    def test_update_grade_by_index_missing(self):
        self._add_student("Ali", 92)
        resp = self.client.put(
            "/api/students/index/0/grade",
            data=json.dumps({}),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 400)

    def test_update_grade_by_index_out_of_range(self):
        resp = self.client.put(
            "/api/students/index/5/grade",
            data=json.dumps({"grade": 95}),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 400)

    # --- size API ---
    def test_size_empty(self):
        resp = self.client.get("/api/students/size")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["size"], 0)

    def test_size_with_data(self):
        self._add_student("Ali", 92)
        self._add_student("Sara", 88)
        resp = self.client.get("/api/students/size")
        self.assertEqual(resp.get_json()["size"], 2)

    # --- average API ---
    def test_average(self):
        self._add_student("Ali", 90)
        self._add_student("Sara", 80)
        resp = self.client.get("/api/students/average")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["average"], 85.0)

    def test_average_empty(self):
        resp = self.client.get("/api/students/average")
        self.assertEqual(resp.get_json()["average"], 0)

    # --- highest API ---
    def test_highest(self):
        self._add_student("Ali", 92)
        self._add_student("Sara", 88)
        resp = self.client.get("/api/students/highest")
        self.assertEqual(resp.get_json()["highest"], 92.0)

    # --- lowest API ---
    def test_lowest(self):
        self._add_student("Ali", 92)
        self._add_student("Sara", 88)
        resp = self.client.get("/api/students/lowest")
        self.assertEqual(resp.get_json()["lowest"], 88.0)


if __name__ == "__main__":
    unittest.main()
