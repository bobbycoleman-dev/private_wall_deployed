from flask_app import app
from flask import flash, render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.message import Message


@app.post("/send_message")
def send_message():
    Message.create(request.form)
    flash("Message sent!")
    return redirect("/dashboard")


@app.route("/delete_message/<int:message_id>")
def delete_message(message_id):
    Message.delete(message_id)
    return redirect("/dashboard")


@app.template_filter("formatdatetime")
def format_datetime(value, format="%b %d %I:%M %p"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.strftime(format)
