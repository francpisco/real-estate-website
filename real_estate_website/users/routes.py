from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from real_estate_website import db, bcrypt
from real_estate_website.models import User, Article
from real_estate_website.users.forms import (LoginForm, RegistrationForm,
                                   RequestResetForm, ResetPasswordForm,
                                   UpdateAccountForm)
from real_estate_website.users.utils import send_reset_email

users = Blueprint("users", __name__)



@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created: You are now able to Log in.", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login unsuccessful. Please check email and password.", "danger")
    return render_template("login.html", title="Log in", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated.", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html", title="Account", form=form)


@users.route("/user/<string:username>")
def user_articles(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    articles = Article.query.filter_by(author=user).order_by(Article.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("user_articles.html", articles=articles, user=user)


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password.", "info")
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", title="Reset Password", form=form)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been updated: You are now able to log in.", "success")
        return redirect(url_for("main.login"))
    return render_template("reset_token.html", title="Reset Password", form=form)
