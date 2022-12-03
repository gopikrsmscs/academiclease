from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


PASSWORD ="root"
PUBLIC_IP_ADDRESS ="34.123.205.220"
DBNAME ="academiclease"
PROJECT_ID ="fit-discipline-369622"
INSTANCE_NAME ="academiclease"
 
app.config["SECRET_KEY"] = "yoursecretkey"
app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket =/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True

db = SQLAlchemy(app)
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    created = db.Column(db.Date, default=datetime.utcnow)

class University(db.Model):
    __tablename__ = "university_list"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200),unique=True)
    url = db.Column(db.String(200))

class posts(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    university_id = db.Column(db.Integer, db.ForeignKey("university_list.id"))
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    created = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(100))



@app.route("/")
def index():
    if not session.get("uname"):
        return redirect("/login")
    return render_template('home.html')
 
 
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("uname")
        password = request.form.get("password")
        session["uname"] = request.form.get("uname")        
        return redirect("/")
    return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    return render_template("signup.html")


@app.route("/logout", methods=["POST", "GET"])
def logout():
    session["uname"] = None
    return redirect("/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)


with app.app_context():
    print("all tables created")
    db.create_all()
