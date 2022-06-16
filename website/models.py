from flask_admin.contrib.sqla import ModelView
from sqlalchemy import desc
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

    def get_growth_info(self):
        return UserGrowthInfo.query.filter_by(id=self.id).first()

    def get_accounting_info(self):
        return UserAccountingInfo.query.filter_by(id=self.id).first()

    def get_volunteer_records(self):
        return VolunteerRecord.query.filter_by(user_id=self.id).order_by(desc(VolunteerRecord.volunteer_date))

    def get_document_requests(self):
        return DocumentRequest.query.filter_by(user_id=self.id).order_by(desc(DocumentRequest.request_date))

    def get_feedbacks(self):
        return Feedback.query.filter_by(to_id=self.id).order_by(desc(Feedback.date))

    def get_payments(self):
        return Payment.query.filter_by(user_id=self.id).order_by(desc(Payment.date))

    def get_volunteer_hours(self, total_hours=0):
        for records in VolunteerRecord.query.filter_by(user_id=self.id):
            total_hours += records.hours
        return round(total_hours, 1)

    def get_user(self, user_id):
        return User.query.filter_by(id=user_id).first()

    def get_all_volunteers(self):
        return User.query.filter_by(permission_level=0)


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
    start_date = db.Column(db.Date)
    school = db.Column(db.String(150))
    birth_date = db.Column(db.Date)
    career = db.Column(db.String(150))
    status = db.Column(db.String(25))
    records = db.relationship("VolunteerRecord")
    requests = db.relationship("DocumentRequest")


class UserGrowthInfo(db.Model):
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    status = db.Column(db.String(150))
    feedback = db.relationship("Feedback", foreign_keys="[Feedback.to_id]")
    traits = db.Column(db.String(150))


class UserAccountingInfo(db.Model):
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    total_paid = db.Column(db.Integer)
    next_payment = db.Column(db.Date)
    payments = db.relationship("Payment")


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    amount = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user_accounting_info.id"))


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    type = db.Column(db.String(150))
    content = db.Column(db.String(150))
    to_id = db.Column(db.Integer, db.ForeignKey("user_growth_info.id"))
    from_id = db.Column(db.Integer, db.ForeignKey("user_growth_info.id"))


class VolunteerRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    volunteer_date = db.Column(db.Date)
    event = db.Column(db.String(150))
    position = db.Column(db.String(150))
    task = db.Column(db.String(150))
    hours = db.Column(db.Integer)
    notes = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey("user_volunteer_info.id"))


class DocumentRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_date = db.Column(db.Date)
    due_date = db.Column(db.Date)
    purpose = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey("user_volunteer_info.id"))


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.permission_level == 5
