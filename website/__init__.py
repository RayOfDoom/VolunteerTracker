from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'testsecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .data import data

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(data, url_prefix='/')

    from .models import User, UserContactInfo, UserVolunteerInfo, AdminView, VolunteerRecord, DocumentRequest, UserGrowthInfo, Feedback, Payment, UserAccountingInfo

    create_database(app)

    admin = Admin(app, template_mode='bootstrap3')
    admin.add_view(AdminView(User, db.session, category='User'))
    admin.add_view(AdminView(UserContactInfo, db.session, category='User'))
    admin.add_view(AdminView(UserVolunteerInfo, db.session, category='User'))
    admin.add_view(AdminView(UserGrowthInfo, db.session, category='User'))
    admin.add_view(AdminView(UserAccountingInfo, db.session, category='User'))
    admin.add_view(AdminView(VolunteerRecord, db.session, category='Volunteer'))
    admin.add_view(AdminView(DocumentRequest, db.session, category='Volunteer'))
    admin.add_view(AdminView(Feedback, db.session, category='Growth'))
    admin.add_view(AdminView(Payment, db.session, category='Accounting'))

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
