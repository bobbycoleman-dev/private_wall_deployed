from flask_app import app
from flask import flash, render_template, redirect, request, session
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.message import Message
from datetime import datetime, time

bcrypt = Bcrypt(app)


@app.route("/")
def index():
    """Render the index route"""

    return render_template("index.html")


@app.post("/register/user")
def register():
    """Register the user with an account"""

    if not User.validate_registration(request.form):
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form["password"])

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash,
    }

    user_id = User.create(data)
    session["user_id"] = user_id
    flash("Thank you for registering!")
    return redirect("/dashboard")


@app.post("/login")
def login():
    """Login into an existing account"""

    if not User.validate_login(request.form):
        return redirect("/")

    user = User.get_by_email(request.form["email"])

    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        # if we get False after checking the password
        flash("Invalid Email/Password", "login")
        return redirect("/")
    # if the passwords matched, we set the user_id into session
    session["user_id"] = user.id
    flash("You are now signed in!")
    return redirect("/dashboard")


@app.route("/dashboard")
def dashboard():
    """Display the user's dashboard"""

    if "user_id" not in session:
        return redirect("/")
    users_to_message = User.get_all_except_current(session["user_id"])
    user = User.get_one(session["user_id"])
    messages = Message.get_all(session["user_id"])
    message_count = Message.get_count(session["user_id"])
    count = message_count[0]
    sent_count = Message.get_sent_count(session["user_id"])
    sent = sent_count[0]
    date = datetime.now()
    current_time = time()
    return render_template(
        "dashboard.html",
        user=user,
        users_to_message=users_to_message,
        messages=messages,
        count=count,
        sent=sent,
        date=date,
        current_time=current_time,
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
