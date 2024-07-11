from flask_login import UserMixin
from sqlalchemy import Date
from sqlalchemy.orm import relationship
from extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    birthdays = relationship("Birthdays", back_populates="author", cascade="all, delete-orphan")


class Birthdays(db.Model):
    __tablename__ = "birthdays"
    id = db.Column(db.Integer, primary_key=True)
    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Create reference to the User object, the "birthday" refers to the birthdays property in the User class.
    author = relationship("User", back_populates="birthdays")
    name = db.Column(db.String(1000), nullable=False)
    date = db.Column(Date, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=False)
