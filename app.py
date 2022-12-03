from flask import Flask, render_template, redirect, request, session
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    if not session.get("uname"):
        return redirect("/login")
    return render_template('home.html')
 
 
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session["uname"] = request.form.get("uname")
        print("jello")
        return redirect("/")
    return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    return render_template("signup.html")


@app.route("/logout", methods=["POST", "GET"])
def logout():
    session["uname"] = None
    return redirect("/")



app.run(host='0.0.0.0', port=80)