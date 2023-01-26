from flask_app.config.MySQLConnection import connect
from flask import flash
from flask_app.models import users
mydb = 'Workout'

class Workout:
    def __init__(self,data):
        self.id = data['id']
        self.activity = data['activity']
        self.duration = data['duration']
        self.positives = data['positives']
        self.negatives = data['negatives']
        self.date = data['date']
        self.users_id = data['users_id']
        self.creator = None
        self.users_who_liked = []

    @staticmethod
    def validate_workout(workout):
        is_valid = True
        if len(workout['activity']) <1:
            flash('Must detail activity completed.')
            is_valid = False
        if len(workout['positives']) <1:
            flash('Must include positives of workout.')
            is_valid = False
        if len(workout['negatives']) <1:
            flash('Must include negatives of workout.')
            is_valid = False
        if len(workout['date']) <1:
            flash('Date must be filled out.')
            is_valid = False
        if len(workout['duration']) <1:
            flash('Duration of workout must be provided.')
            is_valid = False
        print(f"is_valid: {is_valid}")
        return is_valid

    @classmethod
    def save(cls,data):
        query = '''
        INSERT INTO workouts 
        (activity,duration,positives,negatives,date,users_id) 
        VALUES(%(activity)s,%(duration)s,%(positives)s,%(negatives)s,%(date)s,%(user_id)s);'''
        results = connect(mydb).query_db(query, data)
        print(f"results: {results}")
        return results
    
    @classmethod
    def getById(cls, data):
        print(data)
        query = '''
        SELECT * 
        FROM workouts 
        WHERE id = %(id)s;'''
        results = connect(mydb).query_db(query, data)
        print(f"results: {results}")
        return cls(results[0])

    @classmethod
    def get_all_workouts(cls):
        query = '''
        SELECT * FROM workouts 
        JOIN users 
        AS creators 
        ON workouts.users_id = creators.id
        LEFT JOIN likes
        ON workouts.id = likes.workout_id
        LEFT JOIN users
        AS users_who_liked 
        ON likes.user_id = users_who_liked.id;
        '''
        results = connect(mydb).query_db(query)
        workouts = []
        for row in results:

            new_workout = True
            user_who_liked = {
            'id' : row ['users_who_liked.id'],
            'first_name' : row['users_who_liked.first_name'],
            'last_name' : row['users_who_liked.last_name' ],
            'email': row['users_who_liked.email'],
            'password': row['users_who_liked.password'],
            'updated_at': row['users_who_liked.updated_at'],
            'created_at' : row['users_who_liked.created_at'],
            }
            number_of_workouts = len(workouts)
            if number_of_workouts > 0:
                last_workout = workouts[-1]
                if last_workout.id == row['id']:
                    last_workout.users_who_liked.append(users.User(user_who_liked))
                    new_workout = False
            
            if new_workout:
                this_workout = cls(row)
                user_data={
                    'id' : row ['creators.id'],
                    'first_name' : row['first_name'],
                    'last_name' : row['last_name' ],
                    'email': row['email'],
                    'password': row['password'],
                    'updated_at': row['updated_at'],
                    'created_at' : row['created_at'],
                }
                this_user = users.User(user_data)
                this_workout.creator = this_user

                if row['users_who_liked.id']:
                    this_workout.users_who_liked.append(users.User(user_who_liked))

                workouts.append(this_workout)
        return workouts

    @classmethod
    def get_one(cls,data):
        query  = '''
        SELECT * 
        FROM workouts 
        WHERE id = %(id)s'''
        result = connect(mydb).query_db(query, data)
        return cls(result[0])

    @classmethod
    def destroy(cls,data):
        query  = '''
        DELETE 
        FROM workouts 
        WHERE id = %(id)s;'''
        return connect(mydb).query_db(query, data)

    @classmethod
    def update(cls,data):
        query = ''' 
        UPDATE Workout.workouts
        SET activity = %(activity)s, duration = %(duration)s ,
        positives = %(positives)s, negatives = %(negatives)s, date= %(date)s,users_id = %(user_id)s 
        WHERE workouts.id = %(id)s;'''
        return connect(mydb).query_db(query, data)

    @classmethod
    def joinIdWorkout(cls, data):
        query = '''
            SELECT users.first_name, users.last_name, users.email
            FROM users
            JOIN Workout.workouts ON users.id = users_id;
        '''
        results = connect(mydb).query_db(query, data)
        print(f"results: {results}")
        output = cls(results[0])
        for row in results:
            workout_info = {
                id : row['id'],
                "activity" : row['post.activity'],
                "duration" : row['post.duration'],
                "positives" : row['post.positives'],
                "negatives" : row['post.negatives'],
                "date" : row['post.date'],
                #"users_id" : row['users_id'],
            }
            output.workouts.append(Workout)
        print(output)
        return(output)




    @classmethod
    def like (cls,data):
        query='''
        INSERT INTO likes (user_id, workout_id) 
        VALUES(%(user_id)s, %(workout_id)s);'''
        return connect(mydb).query_db(query, data)

    @classmethod
    def unlike (cls,data):
        query='''
        DELETE FROM likes 
        WHERE  user_id= %(user_id)s AND workout_id=%(workout_id)s;
        '''
        return connect(mydb).query_db(query, data)