from flask import Blueprint, render_template, flash, redirect, request, url_for

from real_estate_website.main.forms import ContactForm
from real_estate_website.models import Article
from real_estate_website.users.utils import send_mail
from real_estate_website.config import Config

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    articles = Article.query.order_by(Article.date_posted.desc())
    return render_template("home.html", articles=articles)


@main.route("/about")
def about():
    return render_template("about.html", title="About")


@main.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        subject = form.subject.data
        content = form.content.data
        send_mail(name, email, phone, subject, content)
        flash("An email was sent to our office. We'll try to get back to you as soon as possible. Thank you.", "info")
        return redirect(url_for("main.home"))

    return render_template("contact.html", title="Contact us", form=form)

# TODO: include flash message