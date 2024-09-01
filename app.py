from flask import Flask
from blueprints.main import main_bp
from blueprints.auth import auth_bp
from blueprints.llm import llm_bp
from blueprints.story import story_bp
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from blueprints.models import db  # Import db from models.py

load_dotenv()

app = Flask(__name__)
# Configure the SQLAlchemy part of the app to use PyMySQL
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the app with the SQLAlchemy instance
db.init_app(app)

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(llm_bp)
app.register_blueprint(story_bp)
with app.app_context():
    db.create_all()
if __name__ == '__main__':
    app.run(debug=True)
