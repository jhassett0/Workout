from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import users,workouts
from datetime import datetime
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    if users.User.validate_create(request.form):
        print(request.form['password'])
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data ={
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': pw_hash
        }
        session['user_id'] = users.User.save(data)
        return redirect('/workouts')
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    data = {
        "email" : request.form["email"],
        "password" : request.form["password"]
        }
    user_in_db = users.User.getByEmail(data)
    if user_in_db:
        if bcrypt.check_password_hash(user_in_db.password, request.form['password']):
            session['user_id'] = user_in_db.id 
            return redirect('/workouts')   
        else:
            flash("Invalid Credentials.", 'loginError')
            return redirect('/')
    flash("Invalid Credentials.", 'loginError')
    return redirect('/')

@app.route('/logout')
def logout():
        session.clear()
        return redirect('/')