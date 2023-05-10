from flask import Blueprint, render_template, request

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