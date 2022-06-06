from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class UserContactInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wxid = db.Column(db.String(150))
    phone = db.Column(db.String(25))
    parent_name = db.Column(db.String(150))
    parent_email = db.Column(db.String(150))
    parent_wxid = db.Column(db.String(150))
    parent_phone = db.Column(db.String(25))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class UserVolunteerInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    literacy = db.Column(db.String(25))
    start_date = db.Column(db.String(150))
    school = db.Column(db.String(150))
    birth_date = db.Column(db.String(150))
    career = db.Column(db.String(150))
    status = db.Column(db.String(25))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
