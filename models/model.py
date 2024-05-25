
from ext.ext import db

from datetime import datetime

from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=True, default=datetime.now())
    recipes = db.relationship('Recipe', backref='user', cascade="all, delete-orphan", lazy=True)


class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.String(225), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    submission_date = db.Column(db.DateTime, nullable=True, default=datetime.now())
    approval_status = db.Column(db.Boolean, nullable=False, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ingredients = db.relationship('Ingrediants', backref='recipe', cascade="all, delete-orphan", lazy=True)

class Ingrediants(db.Model):
    __tablename__ = "ingredients"
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(50), nullable=False)
    ammount = db.Column(db.String(50), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=True, default=datetime.now())
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

