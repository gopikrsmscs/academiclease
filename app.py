import email
from flask import Flask, render_template, redirect, request, session,url_for,flash
from flask_session import Session
from database import database
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
Session(app)

@app.route("/")
def index():
    if not session.get("email"):
        return redirect("/login")
    return render_template('home.html')


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
        print(email)
        query="select count(*) from user where email='"+email+"' and password='"+password+"')"
        session['email'] = email
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
        return redirect("/login.html")
    return render_template("signup.html")

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('postid.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = database().get_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect('/')

    return render_template('post.html')

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
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8000)

    


