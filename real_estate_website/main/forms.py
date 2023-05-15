from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Length, Email, Optional


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField("Email address", validators=[DataRequired()])
    phone = StringField("Phone number", validators=[Optional(), Length(min=9, max=15)])
    subject = StringField("Subject", validators=[Optional(), Length(max=50)])
    content = TextAreaField("Content", validators=[DataRequired(), Length(max=500)])
    submit = SubmitField("Send")