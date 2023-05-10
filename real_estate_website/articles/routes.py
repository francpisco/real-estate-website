from flask import (Blueprint, abort, flash, redirect,
                   render_template, request, url_for)
from flask_login import current_user, login_required

from real_estate_website import db
from real_estate_website.models import Article
from real_estate_website.articles.forms import ArticleForm

articles = Blueprint("articles", __name__)


@articles.route("/article/new", methods=["GET", "POST"])
@login_required
def new_article():
    form = ArticleForm()
    if form.validate_on_submit():
        article = Article(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(article)
        db.session.commit()
        flash("Your article has been created!", "success")
        return redirect(url_for("main.home"))
    return render_template("create_article.html", title="New Article",
                           form=form, legend="New Article")


@articles.route("/article/<int:article_id>")
def article(article_id):
    article = db.session.query(Article).get_or_404(article_id)
    return render_template('article.html', title=article.title, article=article)


@articles.route("/article/<int:article_id>/update", methods=["GET", "POST"])
@login_required
def update_article(article_id):
    article = db.session.query(Article).get_or_404(article_id)
    if article.author != current_user:
        abort(403)
    form = ArticleForm()
    if form.validate_on_submit():
        article.title = form.title.data
        article.content = form.content.data
        db.session.commit()
        flash("Your article has been updated!", "success")
        return redirect(url_for("articles.article", article_id=article.id))
    elif request.method == "GET":
        form.title.data = article.title
        form.content.data = article.content
    return render_template("create_article.html", title="Update Article",
                           form=form, legend="Update Article")


@articles.route("/article/<int:article_id>/delete", methods=["POST"])
@login_required
def delete_article(article_id):
    article = db.session.query(Article).get_or_404(article_id)
    if article.author != current_user:
        abort(403)
    db.session.delete(article)
    db.session.commit()
    flash("Your article has been deleted!", "success")
    return redirect(url_for("main.home"))