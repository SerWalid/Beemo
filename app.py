from flask import Flask
from blueprints.main import main_bp
from blueprints.auth import auth_bp
from blueprints.llm import llm_bp
from blueprints.story import story_bp
from blueprints.settings import settings_bp
from blueprints.user import user_bp

from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from blueprints.models import db  # Import db from models.py
from flask_migrate import Migrate
from datetime import timedelta

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Set session duration to 7 days
app.config['PIN_CODE_SESSION_LIFETIME'] = timedelta(minutes=1)  # Set a short-lived session for PIN code

# Configure the SQLAlchemy part of the app to use PyMySQL
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the app with the SQLAlchemy instance
db.init_app(app)
migrate = Migrate(app, db)


# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(llm_bp)
app.register_blueprint(story_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(user_bp)

with app.app_context():
    db.create_all()
if __name__ == '__main__':
    app.run(debug=True)