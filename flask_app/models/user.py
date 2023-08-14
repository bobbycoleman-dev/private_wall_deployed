from flask_app.config.mysql_connection import connect_to_mysql
from flask import flash
import re

DATABASE = "private_wall_db"
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
PASSWORD_REGEX = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"


class User:
    def __init__(self, data) -> None:
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # CREATE
    @classmethod
    def create(cls, data):
        query = """
                INSERT INTO users (first_name, last_name, email, password) 
                VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s );
                """
        results = connect_to_mysql(DATABASE).query_db(query, data)
        return results

    # GET ONE USER
    @classmethod
    def get_one(cls, user_id):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        data = {"user_id": user_id}
        results = connect_to_mysql(DATABASE).query_db(query, data)
        if len(results) == 0:
            return
        return User(results[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connect_to_mysql(DATABASE).query_db(query)
        users = []
        for user in results:
            users.append(User(user))
        return users

    @classmethod
    def get_all_except_current(cls, user_id):
        query = """
                SELECT * FROM users
                WHERE id <> %(user_id)s
                ORDER BY first_name ASC;
                """
        data = {"user_id": user_id}
        results = connect_to_mysql(DATABASE).query_db(query, data)
        users = []
        for user in results:
            users.append(User(user))
        return users

    # GET ONE USER BY EMAIL
    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {"email": email}
        result = connect_to_mysql(DATABASE).query_db(query, data)
        if len(result) < 1:
            return False
        return User(result[0])

    # VALIDATE REGISTRATION FORM
    @staticmethod
    def validate_registration(form_data):
        is_valid = True

        # FIRST NAME
        if len(form_data["first_name"].strip()) == 0:
            flash("Please enter a first name.", "registration")
            is_valid = False
        elif len(form_data["first_name"].strip()) < 2:
            flash("First name must be at least two characters.", "registration")
            is_valid = False
        # LAST NAME
        if len(form_data["last_name"].strip()) == 0:
            flash("Please enter a last name.", "registration")
            is_valid = False
        elif len(form_data["last_name"].strip()) < 2:
            flash("Last name must be at least two characters.", "registration")
            is_valid = False
        # EMAIL VALIDATION
        if len(form_data["email"].strip()) == 0:
            flash("Please enter an email address.", "registration")
            is_valid = False
        elif not EMAIL_REGEX.match(form_data["email"]):
            flash("Invalid email address!", "registration")
            is_valid = False
        elif User.get_by_email(form_data["email"]):
            is_valid = False
            flash(
                "Email already exists. Please enter a new email or login.",
                "registration",
            )
        # PASSWORD
        if len(form_data["password"].strip()) == 0:
            flash("Please enter a password.", "registration")
            is_valid = False

        # User PW regex to check complexity
        elif re.match(PASSWORD_REGEX, form_data["password"]) == None:
            flash(
                "Password must have at least eight characters, one uppercase and lowercase letter, one number, and one special character.",
                "registration",
            )
            is_valid = False
        elif len(form_data["confirm_password"].strip()) == 0:
            flash("Please confirm password.", "registration")
            is_valid = False
        elif form_data["password"] != form_data["confirm_password"]:
            flash("Passwords do not match.", "registration")
            is_valid = False

        return is_valid

    # VALIDATE LOGIN FORM
    @staticmethod
    def validate_login(form_data):
        is_valid = True

        # EMAIL VALIDATION
        if len(form_data["email"].strip()) == 0:
            flash("Please enter an email address.", "login")
            is_valid = False
        elif not EMAIL_REGEX.match(form_data["email"]):
            flash("Invalid email format", "login")
            is_valid = False
        elif not User.get_by_email(form_data["email"]):
            is_valid = False
            flash(
                "Invalid Email/Password.",
                "login",
            )
        # PASSWORD
        if len(form_data["password"].strip()) == 0:
            flash("Please enter a password.", "login")
            is_valid = False
        elif len(form_data["password"].strip()) < 8:
            flash("Password must be at least eight characters.", "login")
            is_valid = False
        return is_valid
