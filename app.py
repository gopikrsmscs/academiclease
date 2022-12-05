from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from database import database

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
Session(app)

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
    if request.method == "POST":
        username = request.form.get("uname")
        password = request.form.get("password")
        retype_paassword = request.form.get("rpassword")
        email = request.form.get("email")
        query="insert into user(name,email,password) values('"+str(username)+"','"+str(email)+"','"+str(password)+"')"
        database_connection = database().get_connection()
        mycursor = database_connection.cursor()
        try:
            mycursor.execute(query)
            database_connection.commit()
        except:
            print("failed")
            print(query)
            database_connection.rollback()
            database_connection.commit()
        database_connection.close()
        session["uname"] = request.form.get("uname") 
        session["email"] = request.form.get("uname") 
        session["id"] = request.form.get("uname")        
        return redirect("/")
    return render_template("signup.html")


@app.route("/logout", methods=["POST", "GET"])
def logout():
    session["uname"] = None
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8000)

    


