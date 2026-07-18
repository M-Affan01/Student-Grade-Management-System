/**
 * API Service Module (Local Storage)
 * ====================================
 * Fully client-side storage using localStorage.
 * No backend required - works on Netlify or any static host.
 */

const STORAGE_KEY = "student_grade_management_data";

function getStoredData() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch {}
  return { students: [], nextId: 1 };
}

function saveStoredData(data) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}

function getAllStudents() {
  return getStoredData().students;
}

function getNextId() {
  const data = getStoredData();
  return data.nextId;
}

function computeStats(students) {
  if (!students.length) {
    return {
      total_students: 0,
      average_grade: 0,
      highest_grade: 0,
      lowest_grade: 0,
      passing: 0,
      failing: 0,
      grade_a: 0,
      grade_b: 0,
      grade_c: 0,
      grade_d: 0,
      grade_f: 0,
    };
  }
  const grades = students.map((s) => s.grade);
  const passing = grades.filter((g) => g >= 60).length;
  return {
    total_students: students.length,
    average_grade: Math.round((grades.reduce((a, b) => a + b, 0) / grades.length) * 100) / 100,
    highest_grade: Math.max(...grades),
    lowest_grade: Math.min(...grades),
    passing,
    failing: students.length - passing,
    grade_a: grades.filter((g) => g >= 90).length,
    grade_b: grades.filter((g) => g >= 80 && g < 90).length,
    grade_c: grades.filter((g) => g >= 70 && g < 80).length,
    grade_d: grades.filter((g) => g >= 60 && g < 70).length,
    grade_f: grades.filter((g) => g < 60).length,
  };
}

function wrap(data) {
  return { data };
}

function reject(msg) {
  return Promise.reject({ response: { data: { error: msg } }, message: msg });
}

export const studentService = {
  getAll: async () => wrap(getAllStudents()),

  getById: async (id) => {
    const student = getAllStudents().find((s) => s.id === id);
    return student ? wrap(student) : reject("Student not found");
  },

  getByIndex: async (index) => {
    const students = getAllStudents();
    return index >= 0 && index < students.length
      ? wrap(students[index])
      : reject("Index out of range");
  },

  create: async (data) => {
    if (!data.name || data.grade === undefined || !data.email || !data.subject) {
      return reject("All fields are required");
    }
    const stored = getStoredData();
    const student = {
      id: stored.nextId,
      name: data.name,
      grade: data.grade,
      email: data.email,
      subject: data.subject,
    };
    stored.students.push(student);
    stored.nextId += 1;
    saveStoredData(stored);
    return wrap(student);
  },

  update: async (id, data) => {
    const stored = getStoredData();
    const index = stored.students.findIndex((s) => s.id === id);
    if (index === -1) return reject("Student not found");
    stored.students[index] = { ...stored.students[index], ...data, id };
    saveStoredData(stored);
    return wrap(stored.students[index]);
  },

  updateGrade: async (index, grade) => {
    const stored = getStoredData();
    if (index < 0 || index >= stored.students.length) return reject("Index out of range");
    stored.students[index].grade = grade;
    saveStoredData(stored);
    return wrap(stored.students[index]);
  },

  delete: async (id) => {
    const stored = getStoredData();
    const index = stored.students.findIndex((s) => s.id === id);
    if (index === -1) return reject("Student not found");
    const removed = stored.students.splice(index, 1)[0];
    saveStoredData(stored);
    return wrap({ message: "Student deleted successfully", student: removed });
  },

  deleteByIndex: async (index) => {
    const stored = getStoredData();
    if (index < 0 || index >= stored.students.length) return reject("Index out of range");
    const removed = stored.students.splice(index, 1)[0];
    saveStoredData(stored);
    return wrap({ message: "Student deleted successfully", student: removed });
  },

  search: async (name) => {
    const results = getAllStudents().filter((s) =>
      s.name.toLowerCase().includes(name.toLowerCase())
    );
    return wrap(results);
  },

  sortByGrade: async (ascending = true) => {
    const sorted = [...getAllStudents()].sort((a, b) =>
      ascending ? a.grade - b.grade : b.grade - a.grade
    );
    return wrap(sorted);
  },

  getStats: async () => wrap(computeStats(getAllStudents())),

  getSize: async () => wrap({ size: getAllStudents().length }),

  getAverage: async () => {
    const students = getAllStudents();
    const avg = students.length
      ? Math.round((students.reduce((a, s) => a + s.grade, 0) / students.length) * 100) / 100
      : 0;
    return wrap({ average: avg });
  },

  getHighest: async () => {
    const students = getAllStudents();
    return wrap({ highest: students.length ? Math.max(...students.map((s) => s.grade)) : 0 });
  },

  getLowest: async () => {
    const students = getAllStudents();
    return wrap({ lowest: students.length ? Math.min(...students.map((s) => s.grade)) : 0 });
  },
};

export const storageService = {
  getInfo: async () =>
    wrap({
      type: "localStorage",
      students_count: getAllStudents().length,
      storage_key: STORAGE_KEY,
    }),

  save: async () => {
    saveStoredData(getStoredData());
    return wrap({ message: "Data saved to browser storage" });
  },

  load: async () => {
    const students = getAllStudents();
    return wrap({ message: "Data loaded from browser storage", count: students.length });
  },
};

export default studentService;
