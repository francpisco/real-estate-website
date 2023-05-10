from datetime import datetime, timezone, timedelta
import jwt
from flask import current_app
from real_estate_website import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    articles = db.relationship('Article', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        reset_token = jwt.encode({
            "user_id": self.id,
            "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expires_sec)
        }, current_app.config["SECRET_KEY"], algorithm="HS256")
        
        return reset_token

    @staticmethod
    def verify_reset_token(token):
        try:
            user_id = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                leeway=timedelta(seconds=10),
                algorithms=["HS256"]
            )["user_id"]
        except:
            return None
        return db.session.query(User).get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_file = db.Column(db.String(20), nullable=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Article('{self.title}', {self.date_posted}')"
