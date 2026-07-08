from flask import Flask, render_template , flash , redirect ,request
from database import db
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "exam_secret_key_123"


db.init_app(app)


class Students(db.Model):
    __tablename__ = "students"

    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    mobile = db.Column(db.BigInteger)
    gender = db.Column(db.String(50))
    address = db.Column(db.String(100))
    birthday = db.Column(db.Date)

    results = db.relationship("Results", back_populates="student" , cascade="all, delete")



@app.route("/")
def home():
    students = Students.query.all()
    return render_template("index.html", students=students)




class Exams(db.Model):
    __tablename__ = "exams"

    exam_id = db.Column(db.Integer, primary_key=True)
    exam_name = db.Column(db.String(100), nullable=False)
    exam_date = db.Column(db.DateTime)

    results = db.relationship("Results", back_populates="exam"  , cascade="all, delete")
    


@app.route("/exams")
def exams():
    exams = Exams.query.all()
    return render_template("exams.html", exams=exams)





@app.route("/exams/add", methods=["GET", "POST"])
def add_exam():

    if request.method == "POST":

        exam = Exams(
            exam_name=request.form["exam_name"],
            exam_date=request.form["exam_date"]
        )

        db.session.add(exam)
        db.session.commit()

        flash("Exam added successfully!")

        return redirect("/exams")

    return render_template("add_exam.html")





@app.route("/exams/edit/<int:id>", methods=["GET", "POST"])
def edit_exam(id):

    exam = Exams.query.get_or_404(id)

    if request.method == "POST":

        exam.exam_name = request.form["exam_name"]
        exam.exam_date = request.form["exam_date"]

        db.session.commit()

        flash("Exam updated successfully!")

        return redirect("/exams")

    return render_template("edit_exam.html",exam=exam)




@app.route("/exams/delete/<int:id>")
def delete_exam(id):

    exam = Exams.query.get_or_404(id)

    db.session.delete(exam)
    db.session.commit()

    flash("Exam deleted successfully!")

    return redirect("/exams")







class Results(db.Model):
    __tablename__ = "results"

    result_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.student_id"))
    exam_id = db.Column(db.Integer, db.ForeignKey("exams.exam_id"))
    score = db.Column(db.Numeric(5, 2))
    student = db.relationship("Students", back_populates="results")
    exam = db.relationship("Exams", back_populates="results")


@app.route("/results")
def results():
    results = Results.query.all()
    return render_template("results.html", results=results)



@app.route("/results/add", methods=["GET", "POST"])
def add_result():

    students = Students.query.all()
    exams = Exams.query.all()

    if request.method == "POST":

        result = Results(
            student_id=request.form["student_id"],
            exam_id=request.form["exam_id"],
            score=request.form["score"]
        )

        db.session.add(result)
        db.session.commit()

        flash("Result added successfully!")

        return redirect("/results")

    return render_template( "add_result.html", students=students, exams=exams
    )



@app.route("/results/edit/<int:id>", methods=["GET", "POST"])
def edit_result(id):

    result = Results.query.get_or_404(id)
    students = Students.query.all()
    exams = Exams.query.all()

    if request.method == "POST":
        result.student_id = request.form["student_id"]
        result.exam_id = request.form["exam_id"]
        result.score = request.form["score"]

        db.session.commit()

        flash("Result updated successfully!")

        return redirect("/results")

    return render_template("edit_result.html", result=result, students=students, exams=exams
    )



@app.route("/results/delete/<int:id>")
def delete_result(id):
    result = Results.query.get_or_404(id)

    db.session.delete(result)
    db.session.commit()

    flash("Result deleted successfully!")

    return redirect("/results")









@app.route("/addstudents" ,  methods=["GET", "POST"])
def addstud():
        if request.method == "POST":

            name=request.form["name"],
            email = request.form["email"],
            mobile = request.form["mobile"],
            gender = request.form["gender"],
            address = request.form["address"],
            birthday = request.form["birthday"]

                
        if not name or not email or not mobile:
            flash("All fields are required!")
            return redirect("/students/add")

        student = Students(
            name=name,
            email=email,
            mobile=mobile,
            gender=gender,
            address=address,
            birthday=birthday
        )
        
        db.session.add(student)
        db.session.commit()

        flash("Student added successfully!")

        return redirect("/")
            
        

        return render_template("add.html")



@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    student = Students.query.get_or_404(id)

    if request.method == "POST":

        student.name = request.form["name"]
        student.email = request.form["email"]
        student.mobile = request.form["mobile"]
        student.gender = request.form["gender"]
        student.address = request.form["address"]
        student.birthday = request.form["birthday"]

        db.session.commit()

        flash("Student updated successfully!")

        return redirect("/")

    return render_template("edit.html", student=student)



@app.route("/delete_student/<int:id>")
def delete_student(id):
    student = Students.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    flash("Student deleted successfully!")

    return redirect("/")
    




with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)