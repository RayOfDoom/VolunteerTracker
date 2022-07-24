from flask import Blueprint, jsonify, make_response, render_template, request, flash, redirect, url_for
from . import db
from .models import User, UserContactInfo, UserVolunteerInfo, UserGrowthInfo, UserAccountingInfo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


def user_login(email, password):
    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.landing'))
        else:
            flash('Incorrect password, try again.', category='error')
    else:
        flash('Email does not exist.', category='error')
    return render_template('login.html', user=current_user)


def user_signup(email, first_name, last_name, password1, password2):
    user = User.query.filter_by(email=email).first()
    if user:
        flash('Email already exists.', category='error')
    elif len(email) < 4 or len(email) > 150:
        flash('Email must be greater than 3 characters.', category='error')
    elif len(first_name) < 2 or len(first_name) > 150:
        flash('First name must be greater than 1 character.', category='error')
    elif len(last_name) < 2 or len(last_name) > 150:
        flash('Last name must be greater than 1 character.', category='error')
    elif password1 != password2:
        flash('The passwords do not match', category='error')
    elif len(password1) < 7 or len(password1) > 150:
        flash('Password must be at least 7 characters', category='error')
    else:
        new_user = User(email=email, first_name=first_name, last_name=last_name,
                        password=generate_password_hash(password1, method='sha256'), permission_level=0)
        db.session.add(new_user)
        db.session.commit()
        db.session.add(UserContactInfo(id=new_user.id))
        db.session.add(UserVolunteerInfo(id=new_user.id))
        db.session.add(UserGrowthInfo(id=new_user.id))
        db.session.add(UserAccountingInfo(id=new_user.id))
        db.session.commit()
        flash('Account created!', category='success')
        login_user(new_user, remember=True)
        return redirect(url_for('views.landing'))
    return render_template('signup.html', user=current_user)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        return user_login(email, password)
    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out.', category='success')
    return redirect(url_for('views.home'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        return user_signup(email, first_name, last_name, password1, password2)
    return render_template('signup.html', user=current_user)


#BACKEND FOR SIGNUP CHECK
@auth.route('/sign-up/check_email')
def check_email():
    if request.args:
        email = str(request.args.get("email"))
        user = User.query.filter_by(email=email).first()

        if user is not None:
            res = make_response(jsonify("err"), 200)
        else:
            res = make_response(jsonify("ok"), 200)
    return res