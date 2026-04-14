# Student Course Management System

Flask-based web application for managing students, courses, and enrollments with full CRUD functionality and relational database design.

---

## Features

- Create, update, delete students and courses
- Enroll students into courses (many-to-many relationship)
- Withdraw students from courses
- Data validation (duplicate entries, constraints)
- Dynamic HTML rendering using Jinja2

---

## Tech Stack

- Python
- Flask
- SQLAlchemy
- SQLite
- HTML, CSS

---

## Project Structure
```
.
├── app.py
├── templates/
├── static/
├── requirements.txt
└── README.md
```


---

## Installation and Setup

```bash
git clone https://https://github.com/24f3002643/student-course-management-system

python -m venv venv

# Linux / Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
python app.py
```
