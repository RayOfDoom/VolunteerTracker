from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import relationship
from . import db
from flask_login import UserMixin, current_user
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    permission_level = db.Column(db.Integer)

    def get_volunteer_info(self):
        return UserVolunteerInfo.query.filter_by(id=self.id).first()

    def get_contact_info(self):
        return UserContactInfo.query.filter_by(id=self.id).first()


class UserContactInfo(db.Model):
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    wxid = db.Column(db.String(150))
    phone = db.Column(db.String(25))
    parent_name = db.Column(db.String(150))
    parent_email = db.Column(db.String(150))
    parent_wxid = db.Column(db.String(150))
    parent_phone = db.Column(db.String(25))


class UserVolunteerInfo(db.Model):
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    literacy = db.Column(db.String(25))
    start_date = db.Column(db.String(150))
    school = db.Column(db.String(150))
    birth_date = db.Column(db.String(150))
    career = db.Column(db.String(150))
    status = db.Column(db.String(25))
    records = relationship("VolunteerRecord")


class VolunteerRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    volunteer_date = db.Column(db.String(150))
    event = db.Column(db.String(150))
    position = db.Column(db.String(150))
    task = db.Column(db.String(150))
    hours = db.Column(db.Integer)
    kudos = db.Column(db.String(150))
    notes = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey("user_volunteer_info.id"))


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.permission_level == 5