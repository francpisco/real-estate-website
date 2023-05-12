from flask import Blueprint, render_template, request
from real_estate_website.main.forms import ContactForm

from real_estate_website.models import Article

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    articles = Article.query.order_by(Article.date_posted.desc())
    return render_template("home.html", articles=articles)


@main.route("/about")
def about():
    return render_template("about.html", title="About")


@main.route("/contact")
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        subject = form.subject.data
        content = form.content.data

    return render_template("contact.html", title="Contact us", form=form)