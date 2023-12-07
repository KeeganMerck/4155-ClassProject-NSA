from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import UniqueConstraint
from datetime import datetime
from sqlalchemy import CheckConstraint


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    imagecategory = db.Column(db.String(50), nullable=False)
    vertical = db.Column(db.Integer, nullable=False)
    horizontal = db.Column(db.Integer, nullable=False)
    firstfacelocation = db.Column(db.String(120), nullable=False)
    secondfacelocation = db.Column(db.String(120), nullable=False)
    rotationvalue = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        CheckConstraint('vertical IN (1, 2, 3)'),
        CheckConstraint('horizontal IN (1, 2, 3, 4)')
    )


class StackEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    data = db.Column(db.Integer, nullable=False)
    __table_args__ = (UniqueConstraint("data", name="image_unique"),)
