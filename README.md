# Student Grade Management System

A console-based and web application to manage student grades using **List ADT** with a **React GUI** frontend, **localStorage** for client-side data persistence, and **MVC Architecture**. Deployable on **Netlify** — no backend or database required.

---

## ADT 1: List - Student Grade Management System

### Mini Project Description

Build a console-based application to manage student grades. The system should allow:
- Adding a new student with name and grade
- Removing a student by index or ID
- Updating a student's grade
- Displaying all students sorted by grade (ascending/descending)
- Searching for a student by name
- Calculating class average, highest, and lowest grade

### Possible Interfaces (API)

| Operation | Method Signature | Description |
|-----------|-----------------|-------------|
| Add | `addStudent(name, grade)` | Adds student to the list |
| Remove | `removeStudent(index)` | Removes student at specified index |
| Update | `updateGrade(index, newGrade)` | Updates grade at specified index |
| Get | `getStudent(index)` | Returns student at index |
| GetAll | `getAllStudents()` | Returns all students |
| Search | `searchByName(name)` | Returns index of student with given name |
| Size | `size()` | Returns number of students |
| Sort | `sortByGrade(ascending)` | Sorts list by grade |
| Stats | `getAverage()` | Returns average grade |

### Libraries

| Purpose | Library |
|---------|---------|
| Core List Implementation | `java.util.ArrayList` (Java) / `list` (Python) |
| Sorting | `Collections.sort()` (Java) / `sorted()` (Python) |
| Input Handling | `java.util.Scanner` (Java) / `input()` (Python) |

### Backend Storage
- In-memory: `ArrayList<Student>` (Java) or `List[Student]` (Python)
- Persistent (optional): JSON file or SQLite database

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React.js 18, CSS3 |
| **Storage** | Browser localStorage (client-side) |
| **Backend** (optional) | Python 3, Flask, Flask-CORS |
| **Database** (optional) | MySQL (XAMPP) / JSON File |
| **Architecture** | MVC (Model-View-Controller) |
| **Testing** | Python unittest (200 tests) |

---

## Project Structure

```
Student Grade Management System/
├── frontend/
│   ├── src/
│   │   ├── components/                  # React Components
│   │   │   ├── StudentForm.js           # Add/Edit form with real-time validation
│   │   │   ├── StudentList.js           # Student table with search/sort/delete
│   │   │   ├── StudentStats.js          # Statistics display + grade distribution chart
│   │   │   ├── ConfirmDialog.js         # Custom delete confirmation dialog
│   │   │   ├── ErrorBoundary.js         # React error boundary
│   │   │   └── Toast.js                # Toast notification system
│   │   ├── services/
│   │   │   └── api.js                   # localStorage-based API service
│   │   ├── App.js                       # Main application component
│   │   └── App.css                      # Complete UI styling
│   └── package.json
├── backend/                             # Optional - for local development
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
└── netlify.toml                         # Netlify deployment config
```

---

## Deploy on Netlify

### Steps:
1. Push this repo to GitHub
2. Go to [app.netlify.com](https://app.netlify.com)
3. Click **"New site from Git"** → select your repo
4. Configure build settings:
   - **Base directory:** `frontend`
   - **Build command:** `npm ci && npm run build`
   - **Publish directory:** `build`
5. Click **Deploy** — done!

All data is stored in the browser's localStorage. No server or database needed.

---

## Setup Instructions

### Option 1: Frontend Only (No Backend Required)

```bash
cd frontend
npm install
npm start
```

Frontend runs on **http://localhost:3000** — all CRUD operations work via localStorage.

### Option 2: With Backend (Optional)

#### Database Setup (XAMPP)

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

#### Backend Setup

```bash
cd backend
pip install flask flask-cors mysql-connector-python
python app.py
```

Backend runs on **http://localhost:5002**

#### Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend runs on **http://localhost:3000**

### Environment Variables (Backend)

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

### Browser localStorage (Default - Frontend)
- Uses `localStorage` API for data persistence
- Data stored in browser under key `student_grade_management_data`
- Auto-saves after every write operation
- Loads on startup
- Auto-incrementing ID counter
- No server or database required

### JSON File (Backend - Optional)
- Saves to `data/students.json`
- Auto-saves after every write operation
- Loads on startup
- Maintains metadata (count, timestamp, version)
- Auto-incrementing ID counter

### MySQL (Backend - Optional)
- Fresh connection per query (avoids stale connections)
- Connection pooling with pool size 3
- 5-second connection timeout
- Auto-creates database and table on startup
- SQL aggregation for statistics (efficient)

### Storage Factory (Backend)
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

### Data Persistence (localStorage)
- All data stored in browser's localStorage
- Persists across page refreshes
- Auto-saves after every operation
- No server or database required
- Works offline

### Backend (Optional)
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
- `services/api.js` - All API service methods with documentation

---

## OST: Operational Specification Template (External Dynamic)

**Actor: User (Teacher/Admin)**

### Scenario 1: Add a new student

| Step | Source | Action | Response |
|------|--------|--------|----------|
| 1 | User | Selects "Add Student" from menu | Show prompt |
| 2 | User | Enters student name | Store name |
| 3 | User | Enters student grade (0-100) | Validate |
| 4 | System | Adds student to list | Confirm added |
| 5 | System | Displays updated student list | Show all |

### Scenario 2: Remove a student

| Step | Source | Action | Response |
|------|--------|--------|----------|
| 1 | User | Selects "Remove Student" | Show list |
| 2 | User | Enters index of student to remove | Validate index |
| 3 | System | Removes student from list | Confirm delete |
| 4 | System | Displays updated list | Show all |

### Scenario 3: View statistics

| Step | Source | Action | Response |
|------|--------|--------|----------|
| 1 | User | Selects "View Statistics" | Calculate |
| 2 | System | Computes average, max, min | Display stats |
| 3 | System | Sorts students by grade | Show sorted |

---

## FST: Functional Specification Template (External Static)

### Class: Student

| Attribute | Type |
|-----------|------|
| `_name` | String |
| `_grade` | int |

| Method | Signature | Description |
|--------|-----------|-------------|
| Constructor | `Student(name: String, grade: int)` | Initialize student |
| Getter | `getName(): String` | Get student name |
| Getter | `getGrade(): int` | Get student grade |
| Setter | `setGrade(newGrade: int): void` | Update grade |
| toString | `toString(): String` | String representation |

### Class: StudentManager

| Attribute | Type |
|-----------|------|
| `students` | List\<Student\> |

| Method | Signature | Description |
|--------|-----------|-------------|
| Constructor | `StudentManager()` | Initialize manager |
| Add | `addStudent(name: String, grade: int): boolean` | Add student to list |
| Remove | `removeStudent(index: int): boolean` | Remove student at index |
| Update | `updateGrade(index: int, newGrade: int): boolean` | Update grade at index |
| Get | `getStudent(index: int): Student` | Get student at index |
| GetAll | `getAllStudents(): List<Student>` | Get all students |
| Search | `searchByName(name: String): int` | Find student by name |
| Size | `size(): int` | Get student count |
| Sort | `sortByGrade(ascending: boolean): void` | Sort by grade |
| Average | `getAverage(): double` | Calculate average |
| Highest | `getHighestGrade(): int` | Get highest grade |
| Lowest | `getLowestGrade(): int` | Get lowest grade |

### Class: Main (UI)

| Method | Signature | Description |
|--------|-----------|-------------|
| Main | `main(args: String[]): void` | Application entry point |
| Menu | `displayMenu(): void` | Show menu options |
| Handler | `handleUserChoice(choice: int): void` | Process user input |

---

## SST: State Specification Template (Internal Dynamic)

### State Machine

```
                ┌─────────────┐
                │    Start    │
                └──────┬──────┘
                       │ Initialize
                       ▼
                ┌─────────────┐
       ┌───────│    Idle     │───────┐
       │       │   (Menu)    │       │
       │       └──────┬──────┘       │
       │              │               │
       │ User selects │ User selects  │ User selects
       │ Add          │ Remove        │ Stats
       ▼              ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   Adding    │ │  Removing   │ │   Viewing   │
│   Student   │ │  Student    │ │   Stats     │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │               │               │
       │ Valid input?  │ Valid index?  │ Calculate
       ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   Student   │ │   Student   │ │    Stats    │
│   Added     │ │   Removed   │ │  Displayed  │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │               │               │
       └───────────────┼───────────────┘
                       ▼
                ┌─────────────┐
                │    Idle     │───────────────┐
                │   (Menu)    │               │
                └──────┬──────┘               │
                       │                      │
                       │ User selects Exit    │
                       ▼                      │
                ┌─────────────┐               │
                │ Terminated  │◄──────────────┘
                └─────────────┘
```

### State Transitions

| Current State | Event | Next State | Action |
|---------------|-------|------------|--------|
| Idle | Select "Add" | Adding Student | Show prompt |
| Adding Student | Valid name + grade | Student Added | Add to list |
| Student Added | Confirmation shown | Idle | Show menu |
| Idle | Select "Remove" | Removing Student | Show list |
| Removing Student | Valid index | Student Removed | Delete |
| Student Removed | Confirmation shown | Idle | Show menu |
| Idle | Select "View Stats" | Viewing Stats | Calculate |
| Viewing Stats | Stats displayed | Idle | Show menu |
| Idle | Select "Exit" | Terminated | End program |

---

## LST: Logic Specification Template (Internal Static)

### Core Logic (Pseudocode)

```
FUNCTION addStudent(name, grade):
    IF name IS NULL OR name.trim() == "" THEN
        PRINT "Error: Name cannot be empty"
        RETURN false
    END IF

    IF grade < 0 OR grade > 100 THEN
        PRINT "Error: Grade must be between 0 and 100"
        RETURN false
    END IF

    newStudent = CREATE Student(name, grade)
    students.add(newStudent)
    PRINT "Student added successfully"
    RETURN true
END FUNCTION

FUNCTION removeStudent(index):
    IF index < 0 OR index >= students.size() THEN
        PRINT "Error: Invalid index"
        RETURN false
    END IF

    removed = students.remove(index)
    PRINT "Removed: " + removed.getName()
    RETURN true
END FUNCTION

FUNCTION updateGrade(index, newGrade):
    IF index < 0 OR index >= students.size() THEN
        PRINT "Error: Invalid index"
        RETURN false
    END IF

    IF newGrade < 0 OR newGrade > 100 THEN
        PRINT "Error: Grade must be between 0 and 100"
        RETURN false
    END IF

    students.get(index).setGrade(newGrade)
    PRINT "Grade updated successfully"
    RETURN true
END FUNCTION

FUNCTION getStudent(index):
    IF index < 0 OR index >= students.size() THEN
        PRINT "Error: Invalid index"
        RETURN NULL
    END IF
    RETURN students.get(index)
END FUNCTION

FUNCTION getAllStudents():
    RETURN students
END FUNCTION

FUNCTION searchByName(name):
    FOR i = 0 TO students.size() - 1:
        IF students.get(i).getName().equals(name) THEN
            RETURN i
        END IF
    END FOR
    RETURN -1
END FUNCTION

FUNCTION size():
    RETURN students.size()
END FUNCTION

FUNCTION sortByGrade(ascending):
    IF ascending THEN
        students.sort(COMPARE BY grade ASCENDING)
    ELSE
        students.sort(COMPARE BY grade DESCENDING)
    END IF
    PRINT "Students sorted successfully"
END FUNCTION

FUNCTION getAverage():
    IF students.isEmpty() THEN
        RETURN 0
    END IF

    total = 0
    FOR each student IN students:
        total = total + student.getGrade()
    END FOR
    RETURN total / students.size()
END FUNCTION

FUNCTION getHighestGrade():
    IF students.isEmpty() THEN
        RETURN 0
    END IF

    highest = students.get(0).getGrade()
    FOR each student IN students:
        IF student.getGrade() > highest THEN
            highest = student.getGrade()
        END IF
    END FOR
    RETURN highest
END FUNCTION

FUNCTION getLowestGrade():
    IF students.isEmpty() THEN
        RETURN 0
    END IF

    lowest = students.get(0).getGrade()
    FOR each student IN students:
        IF student.getGrade() < lowest THEN
            lowest = student.getGrade()
        END IF
    END FOR
    RETURN lowest
END FUNCTION
```

---


