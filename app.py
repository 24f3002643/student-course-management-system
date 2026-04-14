from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, "week7_database.sqlite3")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///week7_database.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)


class Student(db.Model):
    __tablename__ = "student"

    student_id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)

class Course(db.Model):
    __tablename__ = "course"

    course_id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)

class Enrollments(db.Model):
    __tablename__ = "enrollments"

    enrollment_id = db.Column(db.Integer, primary_key=True)
    estudent_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable=False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable=False)



@app.route('/')
def index():
    student = Student.query.all()
    return render_template('index.html', students=student)

@app.route('/student/create', methods=["GET", "POST"])
def create_student():
    if request.method == "GET":
        return render_template("create_student.html")
    
    if request.method == "POST":
        roll = request.form["roll"]
        fname = request.form["f_name"]
        lname = request.form["l_name"]

        existing=Student.query.filter_by(roll_number=roll).first()

        if existing:
            return render_template("exists_student.html")
        
        student = Student(
            roll_number = roll,
            first_name = fname,
            last_name = lname
        )

        db.session.add(student)
        db.session.commit()

        return redirect("/")

@app.route('/student/<int:student_id>/update', methods=["GET", "POST"])
def update_student(student_id):
    if request.method == "GET":
        student = Student.query.filter_by(student_id=student_id).first()
        courses = Course.query.all()
        return render_template("update_student.html", student=student, courses=courses)
    
    if request.method == "POST":
        fname = request.form["f_name"]
        lname = request.form["l_name"]
        cid = int(request.form.get("course"))

        student = Student.query.filter_by(student_id=student_id).first()

        student.first_name = fname
        student.last_name = lname

        existing = Enrollments.query.filter_by(
            estudent_id = student_id,
            ecourse_id = cid
        ).first()

        if not existing:
            enrollment = Enrollments(
                estudent_id = student.student_id,
                ecourse_id = cid
            )
            db.session.add(enrollment)

        db.session.commit()

        return redirect('/')


@app.route('/student/<int:student_id>/delete', methods=["GET"])
def delete_student(student_id):
    Enrollments.query.filter_by(estudent_id=student_id).delete()

    student = Student.query.filter_by(student_id = student_id).first()
    db.session.delete(student)

    db.session.commit()

    return redirect('/')    


@app.route('/student/<int:student_id>', methods=["GET"])
def view_student(student_id):
    student = Student.query.filter_by(student_id=student_id).first()
    course = Course.query.join(Enrollments).filter(Enrollments.estudent_id==student_id).all()

    return render_template("view_student.html", student=student, courses=course)


@app.route('/student/<int:student_id>/withdraw/<int:course_id>', methods=["GET"])
def course_withdraw(student_id, course_id):
    enrollments = Enrollments.query.filter_by(
        estudent_id=student_id,
        ecourse_id=course_id
    ).first()

    db.session.delete(enrollments)
    db.session.commit()

    return redirect('/')


@app.route("/courses", methods=["GET"])
def courses():
    course = Course.query.all()

    return render_template("courses.html", course=course)



@app.route("/course/create", methods=["GET", "POST"])
def create_course():
    if request.method == "GET":
        return render_template("create_course.html")

    if request.method == "POST":
        ccode = request.form["code"]
        cname = request.form["c_name"]
        cdesc = request.form["desc"]

        existing=Course.query.filter_by(course_code=ccode).first()

        if existing:
            return render_template("exists_course.html")
        
        course = Course(
            course_code = ccode,
            course_name = cname,
            course_description = cdesc
        )

        db.session.add(course)
        db.session.commit()

        return redirect("/courses")


@app.route("/course/<int:course_id>/update", methods=["GET", "POST"])
def update_course(course_id):
    if request.method == "GET":
        course = Course.query.filter_by(course_id=course_id).first()
        return render_template("update_course.html", courses=course)
    
    if request.method == "POST":
        cname = request.form["c_name"]
        cdesc = request.form["desc"]

        course = Course.query.filter_by(course_id=course_id).first()

        course.course_name = cname
        course.course_description = cdesc

        db.session.commit()

        return redirect('/courses')
    

@app.route('/course/<int:course_id>/delete', methods=["GET"])
def delete_course(course_id):
    Enrollments.query.filter_by(ecourse_id=course_id).delete()

    course = Course.query.filter_by(course_id = course_id).first()
    db.session.delete(course)

    db.session.commit()

    return redirect('/')


@app.route('/course/<int:course_id>', methods=["GET"])
def view_course(course_id):
    course = Course.query.filter_by(course_id=course_id).first()
    student = Student.query.join(Enrollments).filter(Enrollments.ecourse_id==course_id).all()

    return render_template("view_course.html", courses=course, students=student)




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()