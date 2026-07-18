# Student Grade Management System

A web application to manage student grades using **List ADT** with a **React GUI** frontend and **localStorage** for client-side data persistence. Deployable on **Netlify** or any static host — no backend required.

---

## Live Demo

**[Deploy on Netlify](#deploy-on-netlify)** — just push and it works!

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React.js 18, CSS3 |
| **Storage** | Browser localStorage (client-side) |
| **Backend** (optional) | Python 3, Flask, MySQL/JSON |
| **Architecture** | MVC (Model-View-Controller) |

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
│   │   │   └── api.js                   # localStorage-based API (no backend needed)
│   │   ├── App.js                       # Main application component
│   │   └── App.css                      # Complete UI styling
│   └── package.json
├── backend/                             # Optional - for local development
│   ├── models/
│   │   ├── student.py
│   │   └── student_list.py
│   ├── views/
│   │   └── response.py
│   ├── controllers/
│   │   └── student_controller.py
│   ├── database/
│   │   ├── json_storage.py
│   │   ├── mysql_storage.py
│   │   └── storage_factory.py
│   ├── utils/
│   │   └── validator.py
│   ├── tests/                           # 200 unit tests
│   ├── app.py
│   └── run_tests.py
└── netlify.toml
```

---

## Quick Start (Netlify Deploy)

1. Push this repo to GitHub
2. Go to [app.netlify.com](https://app.netlify.com)
3. Click **"New site from Git"** → select this repo
4. Set build settings:
   - **Base directory:** `frontend`
   - **Build command:** `npm ci && npm run build`
   - **Publish directory:** `build`
5. Click **Deploy** — done!

All data is stored in the browser's localStorage. No server needed.

---

## Local Development

### Frontend Only (No Backend)

```bash
cd frontend
npm install
npm start
```

Frontend runs on **http://localhost:3000** — all CRUD operations work via localStorage.

### With Backend (Optional)

If you want MySQL/JSON file storage instead of localStorage:

```bash
cd backend
pip install flask flask-cors mysql-connector-python
python app.py
```

Backend runs on **http://localhost:5002**

Then update `frontend/src/services/api.js` to use the backend API instead of localStorage.

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

### Data Persistence
- Uses browser localStorage for data storage
- Data persists across page refreshes
- Auto-saves after every operation
- No server or database required

### Input Validation
- **Name:** 2-100 chars, letters only
- **Grade:** 0-100, valid number
- **Email:** Valid format, real email providers only
- **Subject:** Required, letters/spaces/hyphens only
- XSS protection on all inputs

---

## Backend (Optional)

The backend is fully functional and can be used instead of localStorage:

### Storage Options

| Storage | Default | Description |
|---------|---------|-------------|
| **localStorage** | Yes | Client-side, works on Netlify |
| **JSON File** | No | Saves to `data/students.json` |
| **MySQL** | No | Requires XAMPP/MySQL running |

### Backend API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/students` | Get all students |
| `POST` | `/api/students` | Add new student |
| `GET` | `/api/students/:id` | Get student by ID |
| `PUT` | `/api/students/:id` | Update student |
| `DELETE` | `/api/students/:id` | Delete student |
| `GET` | `/api/students/search` | Search by name |
| `GET` | `/api/students/sort` | Sort by grade |
| `GET` | `/api/students/stats` | Full statistics |
| `GET` | `/api/storage/info` | Storage backend info |
| `GET` | `/api/health` | Health check |

### Running Backend Tests

```bash
cd backend
python run_tests.py
```

200 unit tests covering models, validation, API endpoints, and storage.

---

## Environment Variables (Backend)

| Variable | Default | Description |
|----------|---------|-------------|
| `STORAGE_TYPE` | `json` | Storage backend: `json` or `mysql` |

---

## License

MIT
