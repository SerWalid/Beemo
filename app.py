from flask import Flask
from blueprints.main import main_bp
from blueprints.auth import auth_bp
from blueprints.llm import llm_bp
from blueprints.story import story_bp


app = Flask(__name__)

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(llm_bp)
app.register_blueprint(story_bp)


if __name__ == '__main__':
    app.run(debug=True)
