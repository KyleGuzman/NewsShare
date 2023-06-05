from datetime import datetime
from flask_app.models.post import Post
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_bcrypt import Bcrypt
from flask_app import app
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = """
        INSERT INTO users
        (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        results = connectToMySQL('news_share').query_db(query, data)
        return results

    @classmethod
    def get_email(cls, email):
        data = {
            "email": email
        }
        query = """
        SELECT * FROM users
        WHERE email = %(email)s;
        """
        results = connectToMySQL('news_share').query_db(query, data)
        if results:
            result = results[0]
            user = cls(result)
            return user
        else:
            return False

    @staticmethod
    def validate_user(data):
        print("here again!")
        is_valid = True
        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters.", 'register')
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters.", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address.", 'register')
            is_valid = False
        if User.get_email(data['email']):
            flash("Email Address already exists!", 'register')
            is_valid = False
        if len(data['password']) < 2:
            flash("Password must be at least 2 characters.", 'register')
            is_valid = False
        if data['password'] != data['password_check']:
            flash("Password does not match!", 'register')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(data):
        is_valid = True
        found_user = User.get_email(data['email'])
        if found_user:
            if bcrypt.check_password_hash(found_user.password, data['password']):
                return found_user
            else:
                flash("Invalid Email or Password", 'login')
                is_valid = False
        else:
            flash("Invalid Email or Password", 'login')
            is_valid = False
        return is_valid

    @classmethod
    def get_user_archive(cls, id):
        data = {
            "id": id
        }
        query = """
        SELECT * FROM users
        JOIN posts
        ON users.id = posts.user_id
        WHERE users.id = %(id)s;
        """
        results = connectToMySQL('news_share').query_db(query, data)
        if results:
            user = cls(results[0])
            user.posts = []
            for row in results:
                archive_data = {
                    **row,
                    'published_date': row['published_date'].strftime("%B %d, %Y"),
                    'id': row['posts.id'],
                    'created_at': row['posts.created_at'],
                    'updated_at': row['posts.updated_at']
                }
                post = Post(archive_data)
                user.posts.append(post)
            return user

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL('news_share').query_db(query)
        users = []
        for i in results:
            users.append(cls(i))
        return users

    @classmethod
    def follow_user(cls, data):
        query = """
        INSERT INTO follows
        (user_id, follower_id)
        VALUE(%(user_id)s, %(follower_id)s)
        """
        results = connectToMySQL('news_share').query_db(query, data)
        return results

    @classmethod
    def get_followers(cls, id):
        data = {
            "id": id
        }
        query = """
        SELECT users.first_name AS followed, users2.first_name AS follower_fname, users2.last_name AS follower_lname
        FROM users
        JOIN follows
        ON users.id = follows.user_id
        JOIN users AS users2
        ON users2.id = follows.follower_id
        WHERE users.id = %(id)s;
        """
        results = connectToMySQL('news_share').query_db(query, data)
        print(results)
        return results

    @classmethod
    def get_one(cls, id):
        data = {
            "id": id
        }
        query = """
        SELECT * FROM users
        WHERE id = %(id)s;
        """
        results = connectToMySQL('news_share').query_db(query, data)
        result = results[0]
        user = cls(result)
        return user

    @classmethod
    def get_followed(cls, id):
        data = {
            "id": id
        }
        query = """
        SELECT users2.first_name AS follower_fname, users.id AS followed_id, users.first_name AS followed_fname, users.last_name AS followed_lname
        FROM users AS users2
        JOIN follows
        ON users2.id = follows.follower_id
        JOIN users
        ON users.id = follows.user_id
        WHERE users2.id = %(id)s;
        """
        results = connectToMySQL('news_share').query_db(query, data)
        return results

    @classmethod
    def not_followed(cls, id):
        data = {
            "id": id
        }
        query = """
        SELECT * FROM users
        WHERE id NOT IN (SELECT users.id AS followed_id
        FROM users AS users2
        LEFT JOIN follows
        ON users2.id = follows.follower_id
        LEFT JOIN users
        ON users.id = follows.user_id
        WHERE users2.id = %(id)s) AND id != %(id)s;
        """
        results = connectToMySQL('news_share').query_db(query, data)
        return results
