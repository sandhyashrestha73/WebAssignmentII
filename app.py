from flask import Flask, render_template , redirect ,request
from database import db
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

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

    results = db.relationship("Results", back_populates="student")



@app.route("/")
def home():
    students = Students.query.all()
    return render_template("index.html", students=students)




class Exams(db.Model):
    __tablename__ = "exams"

    exam_id = db.Column(db.Integer, primary_key=True)
    exam_name = db.Column(db.String(100), nullable=False)
    exam_date = db.Column(db.DateTime)

    results = db.relationship("Results", back_populates="exam")
    


@app.route("/exams")
def exams():
    exams = Exams.query.all()
    return render_template("exams.html", exams=exams)





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


@app.route("/addstudents" ,  methods=["GET", "POST"])
def addstud():
        if request.method == "POST":

            students = Students(
                name=request.form["name"],
                email = request.form["email"],
                mobile = request.form["mobile"],
                gender = request.form["gender"],
                address = request.form["address"],
                birthday = request.form["birthday"]

           
            
        )

            db.session.add(students)
            db.session.commit()

            return redirect("/")

        return render_template("add.html")




@app.route("/deleteuser/<int:id>")
def deleteuser(id):

    students = Students.query.get_or_404(id)

    db.session.delete(students)
    db.session.commit()

    return redirect("/")



with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)