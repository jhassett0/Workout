from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models import users, workouts
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from datetime import datetime
dateFormat = "%m/%d/%Y %I:%M %p"

@app.route('/workouts')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html', 
        current_user = users.User.getById({'id': session['user_id']}),
        all_workouts = workouts.Workout.get_all_workouts()
        )
    return redirect('/')

@app.route('/workouts/destroy/<int:id>')
def destroy(id):
    data ={
        'id': id
    }
    workouts.Workout.destroy(data)
    return redirect('/workouts')

@app.route('/workouts/edit/<int:id>')
def edit(id):
    data ={ 
    "id":id
    }
    return render_template("edit.html",workouts=workouts.Workout.get_one(data),current_user = users.User.getById({'id': session['user_id']}))

@app.route('/workouts/edit/<int:id>',methods=['POST'])
def update(id):
    if not workouts.Workout.validate_workout(request.form):
        return redirect(f'/workouts/edit/{id}')
    data ={
    "activity" : request.form['activity'],
    "duration" : request.form['duration'],
    "positives" : request.form['positives'],
    "negatives" : request.form['negatives'],
    "date" : request.form['date'],
    "user_id" : session['user_id'],
    "id" : id
    }
    workouts.Workout.update(data)
    return redirect('/workouts')

@app.route('/workout/show/<int:id>')
def show(id):
    data ={ 
        "id":id
    }
    return render_template("workout.html",workouts=workouts.Workout.get_one(data),current_user = users.User.getById({'id': session['user_id']}))

@app.route("/workouts/create")
def workout_create_page():
    if 'user_id' in session:
        return render_template('addnew.html', 
        current_user = users.User.getById({'id': session['user_id']}),
        all_workouts = workouts.Workout.get_all_workouts()
        )
    return render_template("dashboard.html")

@app.route('/post/create',methods=['POST'])
def workout_display_page():
    if not workouts.Workout.validate_workout(request.form):
        return redirect('/workouts/create')
    data = {
        "activity" : request.form['activity'],
        "duration" : request.form['duration'],
        "positives" : request.form['positives'],
        "negatives" : request.form['negatives'],
        "date" : request.form['date'],
        "user_id" : session['user_id'],
        "id" : id
    }
    result = workouts.Workout.save(data)
    print(result)
    return redirect('/workouts')

@app.route('/likes/<int:id>/unlike',methods=['POST'])
def unlike(id):
    data ={ 
    "workout_id":id,
    "user_id":session["user_id"]
    }
    workouts.Workout.unlike(data)
    return redirect ('/workouts')

@app.route('/likes/<int:id>/like',methods=['POST'])
def like(id):
    data ={ 
    "workout_id":id,
    "user_id":session["user_id"]
    }
    workouts.Workout.like(data)
    return redirect ('/workouts')