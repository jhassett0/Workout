from flask_app.config.MySQLConnection import connect
from flask import flash
from pprint import pprint
import re	
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
mydb = 'Workout'

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']
        

    @staticmethod
    def validate_create(request):
        is_valid = True
        if len(request['first_name']) <1:
            flash('Please Enter A First Name', 'regError')
            is_valid = False
        elif len(request['first_name']) <3:
            flash('First Name Must Be Longer Than Two Characters', 'regError')
            is_valid = False
        if len(request['last_name']) <1:
            flash('Please Enter A Last Name', 'regError')
            is_valid = False
        elif len(request['last_name']) <3:
            flash('Last Name Must Be Longer Than Two Characters', 'regError')
            is_valid = False
        if len(request['email']) <1:
            flash('Please Enter A Email Address', 'regError')
            is_valid = False
        elif not EMAIL_REGEX.match(request['email']):
            flash("Invalid email address!", 'regError')
            is_valid = False
        if len(request['password']) <1:
            flash('Please Enter A Password', 'regError')
            is_valid = False
        elif len(request['password']) <8:
            flash('Password Must Be Longer Than Eight Characters', 'regError')
            is_valid = False
        if len(request['passConf']) <1:
            flash('Please Confirm Your Password', 'regError')
            is_valid = False
        elif request['password'] != request['passConf']:
            flash('Passwords Do Not Match', 'regError')
            is_valid = False
        if User.getByEmail(request) != False:
            flash('User already exists in database.', 'regError')
            is_valid = False
        print(f"is_valid: {is_valid}")
        return is_valid

    @classmethod
    def save(cls,data):
        query = '''
        INSERT 
        INTO users (first_name,last_name,email,password) 
        VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s);'''
        results = connect(mydb).query_db(query, data)
        print(f"results: {results}")
        return results
    
    @classmethod
    def get_all(cls):
        query = '''
        SELECT *
        FROM users;'''
        results = connect(mydb).query_db(query)
        output = []
        for row in results:
            output.append(cls(row))
        return output

    @classmethod
    def deleteById(cls, data):
        print(data)
        query = '''
        DELETE FROM 
        users WHERE id = %(id)s;'''
        results = connect(mydb).query_db(query, data)
        print(f"results: {results}")

    @classmethod
    def getById(cls, data):
        print(data)
        query = '''
        SELECT * 
        FROM users 
        WHERE id = %(id)s;'''
        results = connect(mydb).query_db(query, data)
        print(f"results: {results}")
        return cls(results[0])

    @classmethod
    def getByEmail(cls, data):
        print(data)
        query = '''
        SELECT * 
        FROM users 
        WHERE email = %(email)s;'''
        results = connect(mydb).query_db(query, data)
        print(f"results: {results}")
        if len(results) <1:
            return False
        return cls(results[0])