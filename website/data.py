from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import User, UserContactInfo, UserVolunteerInfo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user

data = Blueprint('data', __name__)


@data.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        if request.form.get('update') == 'account_info':
            email = request.form.get('email')
            first_name = request.form.get('firstName')
            last_name = request.form.get('lastName')
            confirm_password = request.form.get('confirm_password')

            user = User.query.filter_by(id=current_user.id).first()

            if not check_password_hash(user.password, confirm_password):
                flash('Your password is incorrect.', category='error')
            elif len(email) != 0 and len(email) < 4 or len(email) > 150:
                flash('Email must be greater than 3 characters.', category='error')
            elif len(first_name) != 0 and len(first_name) < 2 or len(first_name) > 150:
                flash('First name must be greater than 1 character.', category='error')
            elif len(last_name) != 0 and len(last_name) < 2 or len(last_name) > 150:
                flash('Last name must be greater than 1 character.', category='error')
            else:
                if email:
                    user.email = email
                if first_name:
                    user.first_name = first_name
                if last_name:
                    user.last_name = last_name
                flash('Account information successfully updated.', category='success')

        elif request.form.get('update') == 'change_password':
            old_password = request.form.get('old_password')
            new_password1 = request.form.get('new_password1')
            new_password2 = request.form.get('new_password2')

            user = User.query.filter_by(id=current_user.id).first()

            if not check_password_hash(user.password, old_password):
                flash('Your password is incorrect.', category='error')
            elif new_password2 != new_password1:
                flash('The passwords do not match.', category='error')
            elif len(new_password1) < 7 or len(new_password1) > 150:
                flash('Your new password must be at least 7 characters', category='error')
            elif old_password == new_password1:
                flash('Your new password must be different than your old password.', category='error')
            else:
                user.password = generate_password_hash(new_password1, 'sha256')
                db.session.commit()
                flash('Password updated successfully!', category='success')


        elif request.form.get('update') == 'contact_info':
            wxid = request.form.get('wxid')
            phone = request.form.get('phone')
            parent_name = request.form.get('parent_name')
            parent_email = request.form.get('parent_email')
            parent_wxid = request.form.get('parent_wxid')
            parent_phone = request.form.get('parent_phone')

            # INSERT DATA CHECKS HERE
            if 1 == 0:
                pass
            else:
                current_contact_info = UserContactInfo.query.filter_by(user_id=current_user.id).first()
                if current_contact_info:
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
                else:
                    current_contact_info = UserContactInfo(wxid=wxid, phone=phone, parent_name=parent_name, parent_email=parent_email,
                                        parent_wxid=parent_wxid, parent_phone=parent_phone,
                                        user_id=current_user.id)
                    db.session.add(current_contact_info)
                    db.session.commit()
                    flash('Information successfully added!', category='success')
        elif request.form.get('update') == 'volunteer_info':
            literacy = request.form.get('literacy')
            start_date = request.form.get('start_date')
            school = request.form.get('school')
            birth_date = request.form.get('birth_date')
            career = request.form.get('career')
            status = request.form.get('status')

            if 1 == 0:
                pass
            else:
                current_volunteer_info = UserVolunteerInfo.query.filter_by(user_id=current_user.id).first()
                if current_volunteer_info:
                    if literacy:
                        current_volunteer_info.literacy = literacy
                    if start_date:
                        current_volunteer_info.start_date = start_date
                    if school:
                        current_volunteer_info.school = school
                    if birth_date:
                        current_volunteer_info.birth_date = birth_date
                    if career:
                        current_volunteer_info.career = career
                    if status:
                        current_volunteer_info.status = status
                    db.session.commit()
                    flash('Information successfully updated!', category='success')
                else:
                    current_volunteer_info = UserVolunteerInfo(literacy=literacy, start_date=start_date, school=school,
                                                     birth_date=birth_date, career=career, status=status,
                                                     user_id=current_user.id)
                    db.session.add(current_volunteer_info)
                    db.session.commit()
                    flash('Information successfully added!', category='success')

    return render_template('profile.html', user=current_user)
