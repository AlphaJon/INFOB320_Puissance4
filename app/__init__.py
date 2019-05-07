from app.config import Config
from flask import Flask
app = Flask(__name__)
app.config.from_object(Config)

from flask_login import LoginManager
login_manager = LoginManager(app)
login_manager.login_view = "login" #for redirect
login_manager.login_message_category = "warning"
login_manager.login_message = "Please log in to continue" #flash error message

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from app import routes
from app.routes import routes