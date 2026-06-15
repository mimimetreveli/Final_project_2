from ext import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def save():
        db.session.commit()


# Table for managing student likes
likes_table = db.Table(
    'post_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True)
)


# === TABLE 1: SCHOOLS ===
class School(db.Model, BaseModel):
    __tablename__ = "schools"
    id = db.Column(db.Integer(), primary_key=True)
    domain = db.Column(db.String(100), unique=True, nullable=False)

    students = db.relationship('User', backref='school', lazy=True)


# === TABLE 2: USERS ===
class User(db.Model, BaseModel, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    grade = db.Column(db.Integer(), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    school_id = db.Column(db.Integer(), db.ForeignKey('schools.id'), nullable=False)

    posts = db.relationship('Post', backref='author', lazy=True)
    liked_posts = db.relationship('Post', secondary=likes_table, backref=db.backref('liked_by', lazy='dynamic'))

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# === TABLE 3: POSTS ===
class Post(db.Model, BaseModel):
    __tablename__ = "posts"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    img = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    school_id = db.Column(db.Integer(), db.ForeignKey('schools.id'), nullable=False)

    school_context = db.relationship('School', backref='posts')