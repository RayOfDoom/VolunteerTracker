from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html", user=current_user)


@views.route('/landing')
def landing():
    return render_template("landing.html", user=current_user)


@views.route('/portal')
@login_required
def portal():
    return render_template("portal.html", user=current_user)


@views.route('/growth')
@login_required
def growth():
    return render_template("growth.html", user=current_user)
