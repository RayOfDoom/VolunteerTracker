from datetime import datetime, date
from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import User, UserContactInfo, UserVolunteerInfo, VolunteerRecord, DocumentRequest
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user

data = Blueprint('data', __name__)


def update_account_info(email, first_name, last_name, confirm_password):
    user = User.query.filter_by(id=current_user.id).first()
    if not check_password_hash(user.password, confirm_password):
        flash('Your password is incorrect.', category='error')
    elif len(email) != 0 and (len(email) < 4 or len(email)) > 150:
        flash('Email must be greater than 3 characters.', category='error')
    elif len(first_name) != 0 and (len(first_name) < 2 or len(first_name)) > 150:
        flash('First name must be greater than 1 character.', category='error')
    elif len(last_name) != 0 and (len(last_name) < 2 or len(last_name)) > 150:
        flash('Last name must be greater than 1 character.', category='error')
    else:
        if email:
            user.email = email
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        db.session.commit()
        flash('Account information successfully updated.', category='success')


def change_password(old_password, new_password1, new_password2):
    user = User.query.filter_by(id=current_user.id).first()
    if not check_password_hash(user.password, old_password):
        flash('Your password is incorrect.', category='error')
    elif new_password2 != new_password1:
        flash('New passwords do not match.', category='error')
    elif len(new_password1) < 7 or len(new_password1) > 150:
        flash('Your new password must be at least 7 characters', category='error')
    elif old_password == new_password1:
        flash('Your new password must be different than your old password.', category='error')
    else:
        user.password = generate_password_hash(new_password1, 'sha256')
        db.session.commit()
        flash('Password updated successfully!', category='success')


def update_contact_info(wxid, phone, parent_name, parent_email, parent_wxid, parent_phone):
    if len(wxid) != 0 and (len(wxid) < 6 or len(wxid) > 20):
        flash('Wechat ID length must be between 6 and 20 characters.', category='error')
    elif len(phone) != 0 and (len(phone) > 25):
        flash('Phone number is too long.', category='error')
    elif len(parent_name) != 0 and (len(parent_name) < 4 or len(parent_name) > 150):
        flash('Parent name must be at least 3 characters.', category='error')
    elif len(parent_email) != 0 and (len(parent_email) < 4 or len(parent_email) > 150):
        flash('Email must be greater than 3 characters.', category='error')
    elif len(parent_wxid) != 0 and (len(parent_wxid) < 6 or len(parent_wxid) > 20):
        flash('Parent Wechat ID length must be between 6 and 20 characters.', category='error')
    elif len(phone) != 0 and (len(phone) > 25):
        flash('Parent phone number is too long.', category='error')
    else:
        current_contact_info = UserContactInfo.query.filter_by(id=current_user.id).first()
        if wxid:
            current_contact_info.wxid = wxid
        if phone:
            current_contact_info.phone = phone
        if parent_name:
            current_contact_info.parent_name = parent_name
        if parent_email:
            current_contact_info.parent_email = parent_email
        if parent_wxid:
            current_contact_info.parent_wxid = parent_wxid
        if parent_phone:
            current_contact_info.parent_phone = parent_phone
        db.session.commit()
        flash('Information successfully updated!', category='success')


def update_volunteer_info(literacy, start_date, school, birth_date, career, status):
    if len(school) != 0 and (len(school) < 5 or len(school) > 150):
        flash('School name must be at least 5 characters.', category='error')
    elif len(career) != 0 and (len(career) > 150):
        flash('Career too long.', category='error')
    else:
        current_volunteer_info = UserVolunteerInfo.query.filter_by(id=current_user.id).first()
        date_start_date = datetime.strptime(start_date, '%Y-%m-%d')
        date_birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
        if literacy:
            current_volunteer_info.literacy = literacy
        if start_date:
            current_volunteer_info.start_date = date_start_date
        if school:
            current_volunteer_info.school = school
        if birth_date:
            current_volunteer_info.birth_date = date_birth_date
        if career:
            current_volunteer_info.career = career
        if status:
            current_volunteer_info.status = status
        db.session.commit()
        flash('Information successfully updated!', category='success')


def add_volunteer_record(volunteer_date, event, position, task, hours, kudos, notes):
    if not volunteer_date:
        flash('Please enter a volunteer date.', category='error')
    elif not event:
        flash('Please enter the name of the event you volunteered in.', category='error')
    elif not hours:
        flash('Please enter the amount of hours you volunteered.', category='error')
    else:
        date_volunteer_date = datetime.strptime(volunteer_date, '%Y-%m-%d')
        new_record = VolunteerRecord(volunteer_date=date_volunteer_date, event=event, position=position, task=task, hours=hours, kudos=kudos, notes=notes, user_id=current_user.id)
        db.session.add(new_record)
        db.session.commit()
        flash('Volunteer record successfully added!', category='success')
        return redirect(url_for('views.portal'))


def request_document(due_date, purpose):
    if not due_date:
        flash('Please enter a due date for this document.', category='error')
    elif not purpose:
        flash('Please state your purpose for requesting this document.', category='error')
    else:
        date_due_date = datetime.strptime(due_date, '%Y-%m-%d')
        new_request = DocumentRequest(request_date=date.today(), due_date=date_due_date, purpose=purpose, user_id=current_user.id)
        db.session.add(new_request)
        db.session.commit()
        flash('Successfully requested LOR/certificate!', category='success')
        return redirect(url_for('views.portal'))


@data.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        if request.form.get('update') == 'account_info':
            email = request.form.get('email')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            confirm_password = request.form.get('confirm_password')
            update_account_info(email, first_name, last_name, confirm_password)
        elif request.form.get('update') == 'change_password':
            old_password = request.form.get('old_password')
            new_password1 = request.form.get('new_password1')
            new_password2 = request.form.get('new_password2')
            change_password(old_password, new_password1, new_password2)
        elif request.form.get('update') == 'contact_info':
            wxid = request.form.get('wxid')
            phone = request.form.get('phone')
            parent_name = request.form.get('parent_name')
            parent_email = request.form.get('parent_email')
            parent_wxid = request.form.get('parent_wxid')
            parent_phone = request.form.get('parent_phone')
            update_contact_info(wxid, phone, parent_name, parent_email, parent_wxid, parent_phone)
        elif request.form.get('update') == 'volunteer_info':
            literacy = request.form.get('literacy')
            start_date = request.form.get('start_date')
            school = request.form.get('school')
            birth_date = request.form.get('birth_date')
            career = request.form.get('career')
            status = request.form.get('status')
            update_volunteer_info(literacy, start_date, school, birth_date, career, status)
    return render_template('profile.html', user=current_user)


@data.route('/track-hours', methods=['GET', 'POST'])
@login_required
def track_hours():
    if request.method == 'POST':
        volunteer_date = request.form.get('volunteer_date')
        event = request.form.get('event')
        position = request.form.get('position')
        task = request.form.get('task')
        hours = request.form.get('hours')
        kudos = request.form.get('kudos')
        notes = request.form.get('notes')
        return add_volunteer_record(volunteer_date, event, position, task, hours, kudos, notes)
    return render_template('track-hours.html', user=current_user)


@data.route('/request-doc', methods=['GET', 'POST'])
@login_required
def request_doc():
    if request.method == 'POST':
        due_date = request.form.get('due_date')
        purpose = request.form.get('purpose')
        return request_document(due_date, purpose)
    return render_template('request-doc.html', user=current_user)