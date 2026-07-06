from flask import Flask, render_template
from database import db
from config import Config

app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)

class Students(db.Model):
    __tablename__ = "students"

    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    mobile = db.Column(db.BigInteger)
    gender = db.Column(db.String(50))
    address = db.Column(db.String(100))
    birthday = db.Column(db.Date)

@app.route("/")
def home():
    students = Students.query.all()
    return render_template("index.html", students=students)

if __name__ == "__main__":
    app.run(debug=True)