from flask import Flask, request, redirect, url_for, session, render_template_string
import sqlite3

app = Flask(__name__)
app.secret_key = "student-attendance-secret-key"

DATABASE = "/storage/emulated/0/attendance.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL,
            course TEXT NOT NULL,
            semester TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    """)

    conn.commit()
    conn.close()


def require_login():
    if "username" not in session:
        return redirect(url_for("login"))
    return None


def page(title, body):
    return render_template_string(f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>

    <style>
    body {{
        font-family: Arial, sans-serif;
        margin: 0;
        background: #f4f7fb;
        color: #222;
    }}

    header {{
        background: #1f3c88;
        color: white;
        padding: 20px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.15);
    }}

    header h1 {{
        margin: 0 0 15px 0;
        font-size: 24px;
    }}

    nav {{
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }}

    nav a {{
        color: white;
        text-decoration: none;
        padding: 9px 12px;
        border-radius: 6px;
        background: rgba(255,255,255,0.12);
        display: inline-block;
    }}

    nav a:hover {{
        background: rgba(255,255,255,0.25);
    }}

    main {{
        max-width: 1100px;
        margin: 25px auto;
        padding: 0 15px;
    }}

    h2 {{
        margin-bottom: 20px;
    }}

    h3 {{
        margin-top: 0;
    }}

    .card {{
        background: white;
        padding: 20px;
        margin-bottom: 18px;
        border-radius: 12px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.08);
    }}

    .grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 15px;
        margin-bottom: 20px;
    }}

    .stat {{
        background: white;
        padding: 22px 15px;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 4px 14px rgba(0,0,0,0.10);
        border-top: 4px solid #1f3c88;
    }}

    .stat h2 {{
        margin: 5px 0 8px 0;
        font-size: 30px;
        color: #1f3c88;
    }}

 .stat p {{
    margin: 0;
    font-size: 15px;
    color: #555;
    font-weight: bold;
    line-height: 1.3;
}}
    

    label {{
        display: block;
        margin-top: 10px;
        font-weight: bold;
    }}

    input, select {{
        width: 100%;
        box-sizing: border-box;
        padding: 11px;
        margin: 6px 0 14px;
        border: 1px solid #bbb;
        border-radius: 7px;
        font-size: 15px;
    }}

    input:focus, select:focus {{
        outline: none;
        border-color: #1f3c88;
    }}

    button, .button {{
        display: inline-block;
        border: 0;
        padding: 10px 14px;
        border-radius: 7px;
        background: #1f3c88;
        color: white;
        text-decoration: none;
        cursor: pointer;
        margin: 3px;
        font-size: 14px;
    }}

    .button:hover, button:hover {{
        opacity: 0.85;
    }}

    .danger {{
        background: #c0392b;
    }}

    .success {{
        background: #16803c;
    }}

    .warning {{
        background: #d68910;
    }}

    table {{
        width: 100%;
        border-collapse: collapse;
        background: white;
    }}

    th, td {{
        border: 1px solid #ddd;
        padding: 10px;
        text-align: left;
    }}

    th {{
        background: #e8eef8;
        color: #222;
    }}

    tr:nth-child(even) {{
        background: #f8faff;
    }}

    .message {{
        padding: 10px;
        background: #e8f5e9;
        border-radius: 7px;
        margin-bottom: 15px;
    }}

    .error {{
        padding: 10px;
        background: #ffebee;
        border-radius: 7px;
        margin-bottom: 15px;
    }}

    .login-box {{
        max-width: 420px;
        margin: 60px auto;
    }}
    
    .footer {{
    text-align: center;
    padding: 20px;
    margin-top: 30px;
    background: #1f3c88;
    color: white;
    font-size: 14px;
}}

.footer p {{
    margin: 5px 0;
}}
    @media print {{
    header,
    nav,
    .button,
    button {{
        display: none !important;
    }}
    
    body {{
        background: white;
    }}
    
    main {{
        max-width: 100%;
        margin: 0;
        padding: 0;
    }}
    
    .card {{
        box-shadow: none;
        border: none;
    }}
}}

    @media (max-width: 700px) {{
        header {{
            padding: 15px;
        }}

        header h1 {{
            font-size: 21px;
        }}

        nav {{
            gap: 5px;
        }}

        nav a {{
            padding: 8px 10px;
            font-size: 13px;
        }}

        main {{
            margin: 15px auto;
            padding: 0 10px;
        }}

        .grid {{
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }}

       .stat {{
    padding: 20px 8px;
    min-height: 85px;
    box-sizing: border-box;
}}

        .stat h2 {{
            font-size: 24px;
        }}

        .stat p {{
            font-size: 13px;
        }}

        .card {{
            padding: 15px;
        }}

        table {{
            font-size: 13px;
        }}

        th, td {{
            padding: 7px;
        }}

        .button, button {{
            padding: 9px 11px;
            font-size: 13px;
        }}
    }}
    </style>
</head>

<body>
<header>
    {f'''
<header>
    <h1>🎓 Student Attendance Management System</h1>

    <nav>
        <a href="/dashboard">🏠 Dashboard</a>
        <a href="/add-student">➕ Add Student</a>
        <a href="/students">👨‍🎓 Students</a>
        <a href="/report">📊 Report</a>
        <a href="/date-attendance">📅 Date Attendance</a>
        <a href="/date-range">📆 Date Range</a>
        <a href="/low-attendance">⚠️ Low Attendance</a>
        <a href="/logout">🚪 Logout</a>
    </nav>
</header>
''' if session.get("username") else ""}
</header>

<main>
{body}
</main>
<footer class="footer">
    <p>🎓 Student Attendance Management System</p>
    <p>BCA Project</p>
</footer>
</body>
</html>
""")


# =========================
# LOGIN
# =========================

@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        if username == "admin" and password == "1234":
            session["username"] = username
            return redirect(url_for("dashboard"))

        error = "Invalid username or password."

    body = f"""
    <div class="login-box">
        <div class="card">
            <div style="text-align: center;">
    <h2 style="color: #1f3c88; margin-bottom: 8px;">🔐 Welcome Back!</h2>
    <p style="color: #666; margin-top: 0;">
        Student Attendance Management System
    </p>
</div>

            {f'<div class="error">{error}</div>' if error else ""}

            <form method="POST">
                <label>Username</label>
                <input type="text" name="username"
                       placeholder="Enter username" required>

                <label>Password</label>
                <input type="password" name="password"
                       placeholder="Enter password" required>

                <button class="button" type="submit">
                    🔐 Login
                </button>
            </form>
        </div>
    </div>
    """

    return page("Login", body)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():
    check = require_login()
    if check:
        return check

    conn = get_db()

    total_students = conn.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    total_records = conn.execute(
        "SELECT COUNT(*) FROM attendance"
    ).fetchone()[0]

    present = conn.execute(
        "SELECT COUNT(*) FROM attendance WHERE status='Present'"
    ).fetchone()[0]

    absent = conn.execute(
        "SELECT COUNT(*) FROM attendance WHERE status='Absent'"
    ).fetchone()[0]

    if total_records > 0:
        overall_percentage = (present / total_records) * 100
    else:
        overall_percentage = 0

    recent = conn.execute("""
        SELECT attendance.date,
               attendance.status,
               students.name,
               students.roll_no
        FROM attendance
        JOIN students
        ON attendance.student_id = students.id
        ORDER BY attendance.id DESC
        LIMIT 5
    """).fetchall()

    conn.close()

    recent_rows = ""

    for record in recent:
        recent_rows += f"""
        <tr>
            <td>{record['date']}</td>
            <td>{record['name']}</td>
            <td>{record['roll_no']}</td>
            <td>{record['status']}</td>
        </tr>
        """

    if not recent_rows:
        recent_rows = """
        <tr>
            <td colspan="4"
                style="text-align:center; padding:25px;">
                No attendance records yet.
            </td>
        </tr>
        """

    body = f"""
    <div class="card" style="background: linear-gradient(135deg, #1f3c88, #4b74d1); color: white;">
    <h2 style="margin-bottom: 10px;">
        📊 Student Attendance Dashboard
    </h2>

    <p style="font-size: 17px; line-height: 1.5;">
        Welcome to the Student Attendance Management System.
        Manage students, attendance and reports easily.
    </p>
</div>
</div>

    <div class="grid">

        <div class="stat" style="border-top: 5px solid #1f3c88;">
    <div style="font-size: 32px;">👨‍🎓</div>
    <h2>{total_students}</h2>
    <p>Total Students</p>
</div>

        <div class="stat" style="border-top: 5px solid #4b74d1;">
    <div style="font-size: 32px;">📋</div>
    <h2>{total_records}</h2>
    <p>Attendance Records</p>
</div>

        <div class="stat" style="border-top: 5px solid #16803c;">
    <div style="font-size: 32px;">✅</div>
    <h2>{present}</h2>
    <p>Present</p>
</div>

        <div class="stat" style="border-top: 5px solid #c0392b;">
    <div style="font-size: 32px;">❌</div>
    <h2>{absent}</h2>
    <p>Absent</p>
</div>

        <div class="stat" style="border-top: 5px solid #d68910;">
    <div style="font-size: 32px;">📈</div>
    <h2>{overall_percentage:.2f}%</h2>
    <p>Overall Attendance</p>
</div>

    </div>

    <div class="card">
        <h3>⚡ Quick Actions</h3>

        <a class="button" href="/add-student">
            ➕ Add Student
        </a>

        <a class="button" href="/students">
            👨‍🎓 View Students
        </a>

        <a class="button" href="/report">
            📊 Attendance Report
        </a>

        <a class="button warning" href="/low-attendance">
            ⚠️ Low Attendance
        </a>
    </div>

    <div class="card">
        <h3>🕒 Recent Attendance</h3>

        <div style="overflow-x:auto;">
            <table>
                <tr>
                    <th>Date</th>
                    <th>Name</th>
                    <th>Roll No</th>
                    <th>Status</th>
                </tr>

                {recent_rows}
            </table>
        </div>
    </div>
    """

    return page("Dashboard", body)


# =========================
# ADD STUDENT
# =========================

@app.route("/add-student", methods=["GET", "POST"])
def add_student():
    check = require_login()
    if check:
        return check

    if request.method == "POST":
        name = request.form["name"].strip()
        roll_no = request.form["roll_no"].strip()
        course = request.form["course"].strip()
        semester = request.form["semester"].strip()

        conn = get_db()

        existing = conn.execute(
            "SELECT id FROM students WHERE roll_no = ?",
            (roll_no,)
        ).fetchone()

        if existing:
            conn.close()

            body = f"""
            <h2>➕ Add New Student</h2>

            <div class="error">
                ❌ A student with roll number
                <strong>{roll_no}</strong>
                already exists.
            </div>

            <div class="card">
                <h3>📝 Student Details</h3>

                <form method="POST">

                    <label>Student Name</label>
                    <input type="text" name="name"
                           value="{name}" required>

                    <label>Roll Number</label>
                    <input type="text" name="roll_no"
                           value="{roll_no}" required>

                    <label>Course</label>
                    <input type="text" name="course"
                           value="{course}" required>

                    <label>Semester</label>
                    <input type="text" name="semester"
                           value="{semester}" required>

                    <br>

                    <button class="button success" type="submit">
                        💾 Save Student
                    </button>

                    <a class="button" href="/students">
                        ↩️ Back to Student List
                    </a>

                </form>
            </div>
            """

            return page("Add Student", body)

        conn.execute("""
            INSERT INTO students
            (name, roll_no, course, semester)
            VALUES (?, ?, ?, ?)
        """, (name, roll_no, course, semester))

        conn.commit()
        conn.close()

        return redirect(url_for("students"))

    body = """
    <h2>➕ Add New Student</h2>

    <div class="card">
        <h3>📝 Student Details</h3>

        <form method="POST">

            <label>Student Name</label>
            <input type="text" name="name"
                   placeholder="Enter student name" required>

            <label>Roll Number</label>
            <input type="text" name="roll_no"
                   placeholder="Enter roll number" required>

            <label>Course</label>
            <input type="text" name="course"
                   placeholder="Enter course" required>

            <label>Semester</label>
            <input type="text" name="semester"
                   placeholder="Enter semester" required>

            <br>

            <button class="button success" type="submit">
                💾 Save Student
            </button>

            <a class="button" href="/students">
                ↩️ Back to Student List
            </a>

        </form>
    </div>
    """

    return page("Add Student", body)


# =========================
# STUDENT LIST
# =========================

@app.route("/students")
def students():
    check = require_login()
    if check:
        return check

    search = request.args.get("search", "").strip()

    conn = get_db()

    if search:
        students = conn.execute("""
            SELECT *
            FROM students
            WHERE name LIKE ?
               OR roll_no LIKE ?
               OR course LIKE ?
               OR semester LIKE ?
            ORDER BY id DESC
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        )).fetchall()
    else:
        students = conn.execute("""
            SELECT *
            FROM students
            ORDER BY id DESC
        """).fetchall()

    conn.close()

    rows = ""

    for student in students:
        rows += f"""
        <tr>
            <td>{student['id']}</td>

            <td>
                <strong>{student['name']}</strong>
            </td>

            <td>{student['roll_no']}</td>
            <td>{student['course']}</td>
            <td>{student['semester']}</td>

            <td>
                <a class="button"
                   href="/edit/{student['id']}">
                    ✏️ Edit
                </a>

                <a class="button danger"
                   href="/delete-confirm/{student['id']}">
                    🗑️ Delete
                </a>

                <a class="button success"
                   href="/attendance/{student['id']}">
                    📋 Attendance
                </a>
            </td>
        </tr>
        """

    if not rows:
        rows = """
        <tr>
            <td colspan="6"
                style="text-align:center; padding:25px;">
                No students found.
            </td>
        </tr>
        """

    body = f"""
    <h2 style="color: #1f3c88;">
    👨‍🎓 Student List
</h2>

    <div class="card">

        <form method="GET" action="/students">

            <h3 style="color: #1f3c88; margin-bottom: 10px;">
    🔎 Search Students
</h3>

<input
    type="text"
    name="search"
    placeholder="Search by name, roll number or course"
    value="{{ search }}"
    style="width: 100%; max-width: 500px; padding: 12px; border: 1px solid #ccc; border-radius: 8px; box-sizing: border-box;"
>

            <button
    class="button"
    type="submit"
    style="margin-top: 10px;"
>
    🔍 Search
</button>

            <a class="button" href="/students">
                🔄 Clear
            </a>

        </form>

    </div>

    <div class="card">

        <h3>📚 All Students</h3>

        <div style="overflow-x:auto;">

            <table>

                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Roll No</th>
                    <th>Course</th>
                    <th>Semester</th>
                    <th>Actions</th>
                </tr>

                {rows}

            </table>

        </div>
    </div>

    <div class="card">

        <a class="button" href="/add-student">
            ➕ Add New Student
        </a>

        <a class="button" href="/dashboard">
            🏠 Back to Dashboard
        </a>

    </div>
    """

    return page("Student List", body)


# =========================
# EDIT STUDENT
# =========================

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    check = require_login()
    if check:
        return check

    conn = get_db()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    if not student:
        conn.close()
        return "Student not found"

    if request.method == "POST":

        name = request.form["name"].strip()
        roll_no = request.form["roll_no"].strip()
        course = request.form["course"].strip()
        semester = request.form["semester"].strip()

        conn.execute("""
            UPDATE students
            SET name = ?,
                roll_no = ?,
                course = ?,
                semester = ?
            WHERE id = ?
        """, (name, roll_no, course, semester, id))

        conn.commit()
        conn.close()

        return redirect(url_for("students"))

    conn.close()

    body = f"""
    <h2>✏️ Edit Student</h2>

    <div class="card">

        <h3>📝 Update Student Details</h3>

        <form method="POST">

            <label>Student Name</label>

            <input type="text"
                   name="name"
                   value="{student['name']}"
                   required>

            <label>Roll Number</label>

            <input type="text"
                   name="roll_no"
                   value="{student['roll_no']}"
                   required>

            <label>Course</label>

            <input type="text"
                   name="course"
                   value="{student['course']}"
                   required>

            <label>Semester</label>

            <input type="text"
                   name="semester"
                   value="{student['semester']}"
                   required>

            <br>

            <button class="button" type="submit">
                💾 Update Student
            </button>

            <a class="button" href="/students">
                ↩️ Back to Student List
            </a>

        </form>

    </div>
    """

    return page("Edit Student", body)


# =========================
# DELETE CONFIRMATION
# =========================

@app.route("/delete-confirm/<int:id>")
def delete_confirm(id):
    check = require_login()
    if check:
        return check

    conn = get_db()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    if not student:
        return "Student not found"

    body = f"""
    <h2>🗑️ Delete Student</h2>

    <div class="card">

        <h3>⚠️ Confirm Deletion</h3>

        <p>
            Are you sure you want to delete
            <strong>{student['name']}</strong>
            ({student['roll_no']})?
        </p>

        <p>
            This will also remove the student's
            attendance records.
        </p>

        <br>

        <a class="button danger"
           href="/delete/{student['id']}">
            🗑️ Yes, Delete
        </a>

        <a class="button" href="/students">
            ↩️ No, Go Back
        </a>

    </div>
    """

    return page("Delete Student", body)


@app.route("/delete/<int:id>")
def delete_student(id):
    check = require_login()
    if check:
        return check

    conn = get_db()

    conn.execute(
        "DELETE FROM attendance WHERE student_id = ?",
        (id,)
    )

    conn.execute(
        "DELETE FROM students WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("students"))


# =========================
# ATTENDANCE
# =========================

@app.route("/attendance/<int:student_id>", methods=["GET", "POST"])
def attendance(student_id):
    check = require_login()
    if check:
        return check

    conn = get_db()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    if not student:
        conn.close()
        return "Student not found"

    if request.method == "POST":

        date = request.form["date"]
        status = request.form["status"]

        existing = conn.execute("""
            SELECT id
            FROM attendance
            WHERE student_id = ?
            AND date = ?
        """, (student_id, date)).fetchone()

        if existing:

            conn.execute("""
                UPDATE attendance
                SET status = ?
                WHERE id = ?
            """, (status, existing["id"]))

        else:

            conn.execute("""
                INSERT INTO attendance
                (student_id, date, status)
                VALUES (?, ?, ?)
            """, (student_id, date, status))

        conn.commit()

    records = conn.execute("""
        SELECT *
        FROM attendance
        WHERE student_id = ?
        ORDER BY date DESC
    """, (student_id,)).fetchall()

    conn.close()

    total = len(records)

    present = sum(
        1 for record in records
        if record["status"] == "Present"
    )

    absent = sum(
        1 for record in records
        if record["status"] == "Absent"
    )

    percentage = (
        (present / total) * 100
        if total > 0
        else 0
    )

    rows = ""

    for record in records:

        status_class = (
            "success"
            if record["status"] == "Present"
            else "danger"
        )

        rows += f"""
        <tr>
            <td>{record['date']}</td>

            <td>
                <strong class="{status_class}">
                    {record['status']}
                </strong>
            </td>
        </tr>
        """

    if not rows:
        rows = """
        <tr>
            <td colspan="2"
                style="text-align:center; padding:25px;">
                No attendance records yet.
            </td>
        </tr>
        """

    body = f"""
    <h2>📋 Attendance</h2>

    <div class="card">

        <h3>👨‍🎓 Student Details</h3>

        <p>
            <strong>Name:</strong>
            {student['name']}
        </p>

        <p>
            <strong>Roll Number:</strong>
            {student['roll_no']}
        </p>

        <p>
            <strong>Course:</strong>
            {student['course']}
        </p>

        <p>
            <strong>Semester:</strong>
            {student['semester']}
        </p>

    </div>

    <div class="grid">

        <div class="stat">
            <h2>{total}</h2>
            <p>Total Classes</p>
        </div>

        <div class="stat">
            <h2>{present}</h2>
            <p>Present</p>
        </div>

        <div class="stat">
            <h2>{absent}</h2>
            <p>Absent</p>
        </div>

        <div class="stat">
            <h2>{percentage:.2f}%</h2>
            <p>Attendance</p>
        </div>

    </div>

    <div class="card">

        <h3>📝 Mark Attendance</h3>

        <form method="POST">

            <label>Date</label>

            <input type="date"
                   name="date"
                   required>

            <label>Status</label>

            <select name="status" required>

                <option value="Present">
                    Present
                </option>

                <option value="Absent">
                    Absent
                </option>

            </select>

            <button class="button" type="submit">
                💾 Save Attendance
            </button>

        </form>

    </div>

    <div class="card">

        <h3>📅 Attendance History</h3>

        <div style="overflow-x:auto;">

            <table>

                <tr>
                    <th>Date</th>
                    <th>Status</th>
                </tr>

                {rows}

            </table>

        </div>

    </div>

    <div class="card">

        <a class="button" href="/students">
            👨‍🎓 Back to Students
        </a>

        <a class="button" href="/dashboard">
            🏠 Dashboard
        </a>

    </div>
    """

    return page("Attendance", body)


# =========================
# OVERALL REPORT
# =========================

@app.route("/report")
def report():
    check = require_login()
    if check:
        return check

    conn = get_db()

    students = conn.execute("""
        SELECT *
        FROM students
        ORDER BY name
    """).fetchall()

    rows = ""

    for student in students:

        total = conn.execute("""
            SELECT COUNT(*)
            FROM attendance
            WHERE student_id = ?
        """, (student["id"],)).fetchone()[0]

        present = conn.execute("""
            SELECT COUNT(*)
            FROM attendance
            WHERE student_id = ?
            AND status = 'Present'
        """, (student["id"],)).fetchone()[0]

        absent = conn.execute("""
            SELECT COUNT(*)
            FROM attendance
            WHERE student_id = ?
            AND status = 'Absent'
        """, (student["id"],)).fetchone()[0]

        percentage = (
            (present / total) * 100
            if total > 0
            else 0
        )

        rows += f"""
        <tr>
            <td>{student['name']}</td>
            <td>{student['roll_no']}</td>
            <td>{total}</td>
            <td>{present}</td>
            <td>{absent}</td>
            <td>{percentage:.2f}%</td>
            <td>
                <a class="button"
                   href="/student-report/{student['id']}">
                    👤 View
                </a>
            </td>
        </tr>
        """

    conn.close()

    if not rows:
        rows = """
        <tr>
            <td colspan="7"
                style="text-align:center; padding:25px;">
                No students found.
            </td>
        </tr>
        """

    body = f"""
    <h2>📊 Attendance Report</h2>

<div class="card" style="text-align: right;">
    <button class="button" onclick="window.print()">🖨️ Print Report</button>
</div>''

    <div class="card">

        <div style="overflow-x:auto;">

            <table>

                <tr>
                    <th>Name</th>
                    <th>Roll No</th>
                    <th>Total</th>
                    <th>Present</th>
                    <th>Absent</th>
                    <th>Percentage</th>
                    <th>Action</th>
                </tr>

                {rows}

            </table>

        </div>

    </div>
    """

    return page("Attendance Report", body)


# =========================
# STUDENT REPORT
# =========================

@app.route("/student-report/<int:student_id>")
def student_report(student_id):
    check = require_login()
    if check:
        return check

    conn = get_db()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    if not student:
        conn.close()
        return "Student not found"

    records = conn.execute("""
        SELECT *
        FROM attendance
        WHERE student_id = ?
        ORDER BY date DESC
    """, (student_id,)).fetchall()

    conn.close()

    total = len(records)

    present = sum(
        1 for record in records
        if record["status"] == "Present"
    )

    absent = sum(
        1 for record in records
        if record["status"] == "Absent"
    )

    percentage = (
        (present / total) * 100
        if total > 0
        else 0
    )

    rows = ""

    for record in records:
        rows += f"""
        <tr>
            <td>{record['date']}</td>
            <td>{record['status']}</td>
        </tr>
        """

    if not rows:
        rows = """
        <tr>
            <td colspan="2"
                style="text-align:center; padding:25px;">
                No attendance records.
            </td>
        </tr>
        """

    body = f"""
    <h2>📊 Student Report</h2>

<div class="card" style="text-align: right;">
    <button class="button" onclick="window.print()">🖨️ Print Student Report</button>
</div>

    <div class="card">

        <h3>{student['name']}</h3>

        <p>
            <strong>Roll Number:</strong>
            {student['roll_no']}
        </p>

        <p>
            <strong>Course:</strong>
            {student['course']}
        </p>

        <p>
            <strong>Semester:</strong>
            {student['semester']}
        </p>

    </div>

    <div class="grid">

        <div class="stat">
            <h2>{total}</h2>
            <p>Total Classes</p>
        </div>

        <div class="stat">
            <h2>{present}</h2>
            <p>Present</p>
        </div>

        <div class="stat">
            <h2>{absent}</h2>
            <p>Absent</p>
        </div>

        <div class="stat">
            <h2>{percentage:.2f}%</h2>
            <p>Attendance</p>
        </div>

    </div>

    <div class="card">

        <h3>📅 Attendance History</h3>

        <div style="overflow-x:auto;">

            <table>

                <tr>
                    <th>Date</th>
                    <th>Status</th>
                </tr>

                {rows}

            </table>

        </div>

    </div>

    <div class="card">

        <a class="button" href="/report">
            ↩️ Back to Report
        </a>

    </div>
    """

    return page("Student Report", body)


# =========================
# DATE-WISE ATTENDANCE
# =========================

@app.route("/date-attendance", methods=["GET", "POST"])
def date_attendance():
    check = require_login()
    if check:
        return check

    selected_date = request.form.get(
        "date",
        request.args.get("date", "")
    ).strip()

    rows = ""

    if selected_date:

        conn = get_db()

        records = conn.execute("""
            SELECT students.name,
                   students.roll_no,
                   students.course,
                   students.semester,
                   attendance.status
            FROM attendance
            JOIN students
            ON attendance.student_id = students.id
            WHERE attendance.date = ?
            ORDER BY students.name
        """, (selected_date,)).fetchall()

        conn.close()

        for record in records:
            rows += f"""
            <tr>
                <td>{record['name']}</td>
                <td>{record['roll_no']}</td>
                <td>{record['course']}</td>
                <td>{record['semester']}</td>
                <td>{record['status']}</td>
            </tr>
            """

        if not rows:
            rows = """
            <tr>
                <td colspan="5"
                    style="text-align:center; padding:25px;">
                    No attendance found for this date.
                </td>
            </tr>
            """

    result_section = ""

    if selected_date:
        result_section = f"""
        <div class="card">

            <h3>📋 Attendance for {selected_date}</h3>

            <div style="overflow-x:auto;">

                <table>

                    <tr>
                        <th>Name</th>
                        <th>Roll No</th>
                        <th>Course</th>
                        <th>Semester</th>
                        <th>Status</th>
                    </tr>

                    {rows}

                </table>

            </div>

        </div>
        """

    body = f"""
    <h2>📅 Date-wise Attendance</h2>

    <div class="card">

        <form method="POST">

            <label>Select Date</label>

            <input type="date"
                   name="date"
                   value="{selected_date}"
                   required>

            <button class="button" type="submit">
                🔍 View Attendance
            </button>

        </form>

    </div>

    {result_section}
    """

    return page("Date-wise Attendance", body)


# =========================
# DATE RANGE
# =========================

@app.route("/date-range", methods=["GET", "POST"])
def date_range():
    check = require_login()
    if check:
        return check

    start_date = ""
    end_date = ""
    rows = ""

    if request.method == "POST":

        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        conn = get_db()

        records = conn.execute("""
            SELECT attendance.date,
                   students.name,
                   students.roll_no,
                   attendance.status
            FROM attendance
            JOIN students
            ON attendance.student_id = students.id
            WHERE attendance.date BETWEEN ? AND ?
            ORDER BY attendance.date DESC,
                     students.name
        """, (start_date, end_date)).fetchall()

        conn.close()

        for record in records:
            rows += f"""
            <tr>
                <td>{record['date']}</td>
                <td>{record['name']}</td>
                <td>{record['roll_no']}</td>
                <td>{record['status']}</td>
            </tr>
            """

        if not rows:
            rows = """
            <tr>
                <td colspan="4"
                    style="text-align:center; padding:25px;">
                    No attendance records found.
                </td>
            </tr>
            """

    result_section = ""

    if start_date and end_date:
        result_section = f"""
        <div class="card">

            <h3>
                📋 Attendance from
                {start_date}
                to
                {end_date}
            </h3>

            <div style="overflow-x:auto;">

                <table>

                    <tr>
                        <th>Date</th>
                        <th>Name</th>
                        <th>Roll No</th>
                        <th>Status</th>
                    </tr>

                    {rows}

                </table>

            </div>

        </div>
        """

    body = f"""
    <h2>📆 Date Range Attendance</h2>

    <div class="card">

        <form method="POST">

            <label>Start Date</label>

            <input type="date"
                   name="start_date"
                   value="{start_date}"
                   required>

            <label>End Date</label>

            <input type="date"
                   name="end_date"
                   value="{end_date}"
                   required>

            <button class="button" type="submit">
                🔍 View Attendance
            </button>

        </form>

    </div>

    {result_section}
    """

    return page("Date Range", body)


# =========================
# LOW ATTENDANCE
# =========================

@app.route("/low-attendance")
def low_attendance():
    check = require_login()
    if check:
        return check

    conn = get_db()

    students = conn.execute("""
        SELECT *
        FROM students
        ORDER BY name
    """).fetchall()

    rows = ""

    for student in students:

        total = conn.execute("""
            SELECT COUNT(*)
            FROM attendance
            WHERE student_id = ?
        """, (student["id"],)).fetchone()[0]

        present = conn.execute("""
            SELECT COUNT(*)
            FROM attendance
            WHERE student_id = ?
            AND status = 'Present'
        """, (student["id"],)).fetchone()[0]

        percentage = (
            (present / total) * 100
            if total > 0
            else 0
        )

        if percentage < 75:
            rows += f"""
            <tr>
                <td>{student['name']}</td>
                <td>{student['roll_no']}</td>
                <td>{total}</td>
                <td>{present}</td>
                <td>{percentage:.2f}%</td>
            </tr>
            """

    conn.close()

    if not rows:
        rows = """
        <tr>
            <td colspan="5"
                style="text-align:center; padding:25px;">
                🎉 No students have attendance below 75%.
            </td>
        </tr>
        """

    body = f"""
    <h2>⚠️ Low Attendance</h2>

    <div class="card">

        <p>
            Students with attendance below
            <strong>75%</strong>
            are shown below.
        </p>

        <div style="overflow-x:auto;">

            <table>

                <tr>
                    <th>Name</th>
                    <th>Roll No</th>
                    <th>Total Classes</th>
                    <th>Present</th>
                    <th>Attendance</th>
                </tr>

                {rows}

            </table>

        </div>

    </div>
    """

    return page("Low Attendance", body)


init_db()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
