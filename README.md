# Student Grade Management System

A full-stack web application to manage student grades using **List ADT** with a **React GUI** frontend, **Python Flask** backend, **MySQL/JSON** storage, and **MVC Architecture**.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React.js 18, Axios, CSS3 |
| **Backend** | Python 3, Flask, Flask-CORS |
| **Database** | MySQL (XAMPP) / JSON File |
| **Architecture** | MVC (Model-View-Controller) |
| **Testing** | Python unittest (200 tests) |

---

## Project Structure

```
Student Grade Management System/
├── backend/
│   ├── models/                          # MVC - Model Layer
│   │   ├── student.py                   # Student class with properties, validation, serialization
│   │   └── student_list.py              # List ADT implementation for Student objects
│   ├── views/                           # MVC - View Layer
│   │   └── response.py                  # Standardized JSON response formatting
│   ├── controllers/                     # MVC - Controller Layer
│   │   └── student_controller.py        # Flask Blueprint with all route handlers
│   ├── database/                        # Storage Abstraction Layer
│   │   ├── json_storage.py              # JSON file-based persistence
│   │   ├── mysql_storage.py             # MySQL database persistence
│   │   └── storage_factory.py           # Factory pattern for storage selection
│   ├── utils/
│   │   └── validator.py                 # Input validation & XSS protection
│   ├── tests/                           # Unit Tests (200 tests)
│   │   ├── test_student.py              # Student model tests
│   │   ├── test_student_list.py         # List ADT tests
│   │   ├── test_validator.py            # Validation tests
│   │   ├── test_api.py                  # API endpoint tests
│   │   └── test_json_storage.py         # JSON storage tests
│   ├── app.py                           # Flask application entry point
│   └── run_tests.py                     # Test runner
└── frontend/
    ├── src/
    │   ├── components/                  # React Components
    │   │   ├── StudentForm.js           # Add/Edit form with real-time validation
    │   │   ├── StudentList.js           # Student table with search/sort/delete
    │   │   ├── StudentStats.js          # Statistics display + grade distribution chart
    │   │   ├── ConfirmDialog.js         # Custom delete confirmation dialog
    │   │   ├── ErrorBoundary.js         # React error boundary
    │   │   └── Toast.js                # Toast notification system
    │   ├── services/
    │   │   └── api.js                   # Axios API client with JSDoc
    │   ├── App.js                       # Main application component
    │   └── App.css                      # Complete UI styling
    └── package.json
```

---

## Setup Instructions

### 1. Database Setup (XAMPP)

1. Start **Apache** and **MySQL** from XAMPP Control Panel
2. The database `student_grade_db` and `students` table are created automatically on first run
3. Table schema:

```sql
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    grade DECIMAL(5,2) NOT NULL,
    email VARCHAR(150),
    subject VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 2. Backend Setup

```bash
cd backend
pip install flask flask-cors mysql-connector-python
python app.py
```

Backend runs on **http://localhost:5002**

### 3. Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend runs on **http://localhost:3000**

### 4. Environment Variables (Optional)

| Variable | Default | Description |
|----------|---------|-------------|
| `STORAGE_TYPE` | `json` | Storage backend: `json` (default) or `mysql` |

---

## MVC Architecture

### Model (`models/`)

**`Student` class** - Represents a single student entity with:
- Properties: `id`, `name`, `grade`, `email`, `subject`
- Validation on `name` setter (2-100 chars, letters only)
- Validation on `grade` setter (0-100 range)
- `to_dict()` for JSON serialization
- `from_dict()` class method for deserialization
- `get_letter_grade()` converts numerical grade to letter (A/B/C/D/F)
- `is_passing()` checks if grade >= 60

**`StudentList` class** - List ADT implementation:
- `add_student(name, grade, email, subject)` - Add with validation
- `remove_student(index)` - Remove by index with bounds check
- `update_student(index, name, grade, email, subject)` - Partial update
- `get_student(index)` - Get by index
- `get_all_students()` - Returns a copy (encapsulation)
- `search_by_name(name)` - Case-insensitive partial match
- `size()` - Total count
- `sort_by_grade(ascending)` - In-place sort
- `sort_by_name(ascending)` - Alphabetical sort
- `get_average()`, `get_highest_grade()`, `get_lowest_grade()`
- `get_passing_students()`, `get_failing_students()`
- `get_statistics()` - Comprehensive stats dict
- `to_list()` - Convert to dict list

### View (`views/`)

**`response.py`** - Standardized response formatting:
- `student_to_dict(student)` - Single student to dict
- `student_list_to_dict(students)` - List to dict list
- `success_response(message, data, status)` - Success tuple
- `error_response(message, details, status)` - Error tuple
- `stats_view(stats)` - Statistics formatting
- `sort_view(students, ascending)` - Sort result formatting
- `search_view(results, query)` - Search result formatting
- `storage_info_view(storage_type, storage)` - Storage info formatting

### Controller (`controllers/`)

**`student_controller.py`** - Flask Blueprint with 17 route handlers using `current_app.storage` for dynamic storage access.

### App (`app.py`)

**`create_app()`** factory function:
- Initializes CORS, storage, blueprint registration
- Configures 404, 405, 500, and generic Exception handlers
- Manages storage info, save, load, and health check routes

---

## API Endpoints

### Student CRUD Operations

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|-------------|
| `GET` | `/api/students` | Get all students | - |
| `POST` | `/api/students` | Add new student | `{name, grade, email, subject}` |
| `GET` | `/api/students/:id` | Get student by ID | - |
| `PUT` | `/api/students/:id` | Update student | `{name, grade, email, subject}` |
| `DELETE` | `/api/students/:id` | Delete student by ID | - |

### Index-Based Operations (List ADT)

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|-------------|
| `GET` | `/api/students/index/:index` | Get student by index | - |
| `DELETE` | `/api/students/index/:index` | Delete by index | - |
| `PUT` | `/api/students/index/:index/grade` | Update grade by index | `{grade}` |

### Search & Sort

| Method | Endpoint | Description | Query Params |
|--------|----------|-------------|-------------|
| `GET` | `/api/students/search` | Search by name | `?name=query` |
| `GET` | `/api/students/sort` | Sort by grade | `?ascending=true` |

### Statistics

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/students/stats` | Full statistics with grade distribution |
| `GET` | `/api/students/size` | Total student count |
| `GET` | `/api/students/average` | Average grade |
| `GET` | `/api/students/highest` | Highest grade |
| `GET` | `/api/students/lowest` | Lowest grade |

### Storage & System

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/storage/info` | Storage backend info |
| `POST` | `/api/storage/save` | Manual save (JSON) |
| `POST` | `/api/storage/load` | Manual load (JSON) |
| `GET` | `/api/health` | Health check |

---

## Input Validation Rules

### Name
- Required (cannot be empty)
- 2-100 characters
- Only letters, spaces, hyphens, apostrophes, and periods
- XSS patterns blocked

### Grade
- Required (cannot be None or empty)
- Must be a valid number (int or float)
- Between 0 and 100 inclusive
- Maximum 2 decimal places

### Email (Required)
- Required (cannot be empty)
- Max 150 characters
- Must match standard email format (`local@domain.tld`)
- **Domain whitelist** - only real email providers allowed:
  - `gmail.com`, `yahoo.com`, `yahoo.co.uk`, `yahoo.co.in`
  - `hotmail.com`, `outlook.com`, `live.com`
  - `icloud.com`, `protonmail.com`, `zoho.com`
  - `aol.com`, `mail.com`, `fastmail.com`, and more
- Local part must be at least 3 characters
- Cannot start/end with dots or have consecutive dots
- XSS patterns blocked

### Subject
- Required (cannot be empty)
- Max 100 characters
- Only letters, spaces, and hyphens
- XSS patterns blocked

### XSS Protection
All inputs are checked against these forbidden patterns:
- `<script>` tags
- `javascript:` protocol
- Event handlers (`onclick=`, `onload=`, etc.)
- `<iframe>`, `<object>`, `<embed>` tags

---

## Storage Backends

### JSON File (Default)
- Saves to `data/students.json`
- Auto-saves after every write operation
- Loads on startup
- Maintains metadata (count, timestamp, version)
- Auto-incrementing ID counter

### MySQL (Optional)
- Fresh connection per query (avoids stale connections)
- Connection pooling with pool size 3
- 5-second connection timeout
- Auto-creates database and table on startup
- SQL aggregation for statistics (efficient)

### Storage Factory
- Selects JSON when no storage type is configured
- Uses MySQL when `STORAGE_TYPE=mysql` is configured
- Falls back to JSON if requested MySQL storage is unreachable

---

## Features

### Frontend
- Modern gradient UI with glassmorphism effects
- Add/Edit students with form validation
- Real-time field-level validation feedback
- Search by name (instant filtering)
- Sort by ID, Name, or Grade (ascending/descending)
- Class statistics with animated grade distribution chart
- Custom delete confirmation dialog with backdrop blur
- Toast notifications (success/error/info)
- Error boundary for crash handling
- Responsive design (mobile-friendly)
- Smooth scroll to form on Edit click
- Green pulsing dot for storage connection status

### Backend
- RESTful API with 17 endpoints
- Input validation on all fields
- XSS protection and HTML escaping
- Duplicate name detection
- CORS enabled
- JSON error responses with details
- 404, 405, 500 error handlers
- Health check endpoint
- Storage info endpoint
- 200 unit tests (all passing)

---

## Running Tests

```bash
cd backend
python run_tests.py
```

### Test Coverage

| Test File | Tests | Coverage |
|-----------|-------|----------|
| `test_student.py` | 24 | Student model, properties, serialization |
| `test_student_list.py` | 34 | List ADT CRUD, search, sort, statistics |
| `test_validator.py` | 38 | Name, grade, email, subject, XSS validation |
| `test_api.py` | 50 | All API endpoints, error handling, status codes |
| `test_json_storage.py` | 54 | JSON persistence, CRUD, edge cases |
| **Total** | **200** | **All passing** |

---

## Documentation

All functions include comprehensive **docstrings** with:
- Function purpose and description
- Parameter documentation (name, type, default, description)
- Return value documentation
- Exception/error documentation
- Usage examples where applicable

### Backend Files with Docstrings
- `models/student.py` - Student class and all methods
- `models/student_list.py` - List ADT and all operations
- `utils/validator.py` - All validation methods with rule details
- `database/json_storage.py` - JSON storage CRUD operations
- `database/mysql_storage.py` - MySQL storage CRUD operations
- `database/storage_factory.py` - Factory function documentation
- `controllers/student_controller.py` - All 17 route handlers
- `views/response.py` - Response formatting functions
- `app.py` - Application factory and configuration

### Frontend Files with JSDoc
- `services/api.js` - All API service methods with `@param` and `@returns`
