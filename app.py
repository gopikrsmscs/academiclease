import email
import imp
from flask import Flask, render_template, redirect, request, session,url_for,flash
from flask_session import Session
from database import database
from werkzeug.exceptions import abort
from google.cloud import storage
from werkzeug.utils import secure_filename
import os
import datetime

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= 'fit-discipline-369622-3439a0abb372.json'
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
Session(app)

@app.route("/")
def index():
    if not session.get("email"):
        return redirect("/login")
    else:
        database_connection = database().get_connection()
        mycursor = database_connection.cursor()
        query = "select * from room_post;"
        try:
            mycursor.execute(query)
            posts = mycursor.fetchall()
            database_connection.commit()
        except:
            print("failed")
            print(query)
            database_connection.rollback()
            database_connection.commit()
        database_connection.close() 
        return render_template('home.html',posts=posts)


def get_post(post_id):
    conn = database().get_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post
 
 
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        query="select * from user where email='"+email+"' and password='"+password+"';"
        session['email'] = email
        database_connection = database().get_connection()
        mycursor = database_connection.cursor()
        try:
            mycursor.execute(query)
            output = mycursor.fetchone()
            if output is None:
                flash('Invalid email or password.')
                return render_template("login.html")
            else:
                session['name'] = output[1]
                session['id'] = output[0]
                session['url'] = output[5]
                database_connection.commit()
        except:
            print("failed")
            print(query)
            database_connection.rollback()
            database_connection.commit()
        return redirect("/")
    return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form.get("uname")
        password = request.form.get("password")
        file = request.files["share_files"]
        file.save(secure_filename(file.filename))
        client = storage.Client("fit-discipline-369622")
        bucket = client.get_bucket("academicleaseimages")
        blob = bucket.blob(file.filename)
        blob.upload_from_filename(file.filename)

        retype_paassword = request.form.get("rpassword")
        os.remove(file.filename)
        email = request.form.get("email")
        imageurl = "https://storage.googleapis.com/academicleaseimages/"+file.filename
        query="insert into user(name,email,password,image_url) values('"+str(username)+"','"+str(email)+"','"+str(password)+"','"+str(imageurl)+"')"
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
        return redirect("/login")
    return render_template("signup.html")

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('postid.html', post=post)


@app.route('/createpost', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        status = request.form.get('status')
        id = session["name"]
        image = session["url"]
        univesity_id = request.form.get('university_id')
        if not title:
            flash('Title is required!')
        else:
            connection = database().get_connection()
            conn =connection.cursor()
            image = session["url"]
            query = "INSERT INTO room_post (user, university,title,body,status,image_url) VALUES ('{}','{}','{}','{}','{}','{}')".format(id, univesity_id,title,body,status,image)
            print(query)
            conn.execute(query)
            connection.commit()
            connection.close()
            return redirect("/")
    else:
        university_list = []
        database_connection = database().get_connection()
        mycursor = database_connection.cursor()
        query = "select * from university_list;"
        try:
            mycursor.execute(query)
            university_list = mycursor.fetchall()
            print(university_list[0])
            database_connection.commit()
        except:
            print("failed")
            print(query)
            database_connection.rollback()
            database_connection.commit()
        database_connection.close()  
    return render_template('post.html',university_list=university_list)

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            conn = database().get_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect('/')

    return render_template('editpost.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = database().get_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect('/')


@app.route("/logout", methods=["POST", "GET"])
def logout():
    session["email"] = None
    session["name"] = None
    session["id"] = None
    session['url'] = None
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8000)

    


