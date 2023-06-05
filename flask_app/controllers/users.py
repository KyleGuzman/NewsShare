from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/register_page')
def register_page():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    print(request.form)
    if not User.validate_user(request.form):
        return redirect('register_page')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    session['first_name'] = data['first_name']
    session['id'] = User.create(data)
    return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def login():
    user_logged_in = User.validate_login(request.form)
    if not user_logged_in:
        return redirect('/')
    session['id'] = user_logged_in.id
    session['first_name'] = user_logged_in.first_name
    return redirect('/dashboard')


@app.route('/dashboard')
def show_dashboard():
    if 'first_name' not in session:
        return redirect('/')
    users = User.get_all()
    followed = User.get_followed(session['id'])
    tofollow = User.not_followed(session['id'])
    print(followed)
    print(tofollow)
    return render_template('/dashboard.html', users=users, followed=followed, tofollow=tofollow)


@app.route('/follow', methods=['POST'])
def follow_user():
    User.follow_user(request.form)
    return redirect(f"/archive/{request.form['user_id']}")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
