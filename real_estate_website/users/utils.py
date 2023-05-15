import os
import secrets
import smtplib
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from real_estate_website import mail
from real_estate_website.config import Config


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, "static/profile_pics", picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request",
                  sender="noreply@demo.com",
                  recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
{url_for("users.reset_token", token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
"""
    mail.send(msg)

def send_mail(name, email, phone, subject, body):
    formatted_subject = f"REWebsite - {name}, {email}, {phone}, {subject}"
    msg = Message(subject=formatted_subject, sender="fmpapt-noreply@gmail.com", recipients=["fmpapt@gmail.com"])
    msg.body = body
    mail.send(msg)

    