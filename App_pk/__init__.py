import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
app.config['SECRET_KEY'] = '1234567'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Te rugam sa te loghezi pentru a accesa aceasta pagina.'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)
limiter = Limiter(
    key_func = get_remote_address,
    app = app,
    default_limits = ["200 per day", "50 per hour"],
    strategy="fixed-window",
    storage_uri="memory://"
)

# Importul rutelor la final este "cheia" care rezolvă eroarea circulară
from App_pk import routes