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
            pass
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
            if len(wxid) < 6 or len(wxid) > 20:
                flash('Wechat ID must be between 6 and 20 characters.', category='error')
            elif len(phone) < 3 or len(phone) > 20:
                flash('Phone number must be between 3 and 20 characters.', category='error')
            elif len(parent_name) < 4 or len(parent_name) > 150:
                flash('Parent name must be greater than 3 characters', category='error')
            elif len(parent_email) < 4 or len(parent_email) > 150:
                flash('Parent email must be greater than 3 characters', category='error')
            elif len(parent_phone) < 3 or len(parent_phone) > 20:
                flash('Parent phone number must be between 3 and 20 characters.', category='error')
            else:
                current_info = UserContactInfo.query.filter_by(user_id=current_user.id).first()
                if current_info:
                    current_info.wxid = wxid
                    current_info.phone = phone
                    current_info.parent_name = parent_name
                    current_info.parent_email = parent_email
                    current_info.parent_wxid = parent_wxid
                    current_info.parent_phone = parent_phone
                    db.session.commit()
                    flash('Information successfully updated!', category='success')
                else:
                    db.session.add(
                        UserContactInfo(wxid=wxid, phone=phone, parent_name=parent_name, parent_email=parent_email,
                                        parent_wxid=parent_wxid, parent_phone=parent_phone,
                                        user_id=current_user.id))
                    db.session.commit()
                    flash('Information successfully added!', category='success')
        elif request.form.get('update') == 'volunteer_info':
            literacy = request.form.get('literacy')
            start_date = request.form.get('start_date')
            school = request.form.get('school')
            birth_date = request.form.get('birth_date')
            career = request.form.get('career')
            status = request.form.get('status')

            if len(school) < 3 or len(school) > 150:
                flash('Name of school must be greater than 3 characters', category='error')
            else:
                current_info = UserVolunteerInfo.query.filter_by(user_id=current_user.id).first()
                if current_info:
                    current_info.literacy = literacy
                    current_info.start_date = start_date
                    current_info.school = school
                    current_info.birth_date = birth_date
                    current_info.career = career
                    current_info.status = status
                    db.session.commit()
                    flash('Information successfully updated!', category='success')
                else:
                    db.session.add(UserVolunteerInfo(literacy=literacy, start_date=start_date, school=school,
                                                     birth_date=birth_date, career=career, status=status,
                                                     user_id=current_user.id))
                    db.session.commit()
                    flash('Information successfully added!', category='success')

    return render_template('profile.html', user=current_user)
