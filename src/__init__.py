from decouple import config
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager # Add this line
from src.accounts.models import User # Add this line

app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Registering blueprints
from src.accounts.views import accounts_bp
from src.core.views import core_bp

app.register_blueprint(accounts_bp)
app.register_blueprint(core_bp)

login_manager = LoginManager()  # Add this line
login_manager.init_app(app)  # Add this line

login_manager.login_view = "accounts.login"
login_manager.login_message_category = "danger"
'''
Next, we need to provide a user_loader callback. This callback is used to reload the user object from the user ID stored in the session. It should take the ID of a user, and return the corresponding user object.
'''
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()
