# from website import db, login_manager
from . import db
from datetime import date, datetime
from flask_login import UserMixin
from flask import current_app
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    expenses = db.relationship('Expense', backref='user', lazy=True)


class Expense(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable = False)
    amount = db.Column(db.Float, nullable = False)
    label = db.Column(db.String(50), nullable = False)
    date_created = db.Column(db.DateTime(timezone=True), default = func.now())
    limit = db.Column(db.Float, nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)