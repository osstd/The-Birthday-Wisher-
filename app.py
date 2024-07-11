from flask import Flask
from config import Config
from extensions import db, migrate, login_manager, bootstrap, csrf, limiter
from auth.routes import auth_bp
from main.routes import main_bp
from main.birthdayroutes import birthdays_bp
from models.models import User


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)

    register_extensions(flask_app)
    register_blueprints(flask_app)

    with flask_app.app_context():
        db.create_all()

    return flask_app


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


def register_extensions(flask_app):
    db.init_app(flask_app)
    migrate.init_app(flask_app, db)
    login_manager.init_app(flask_app)
    bootstrap.init_app(flask_app)
    csrf.init_app(flask_app)
    limiter.init_app(flask_app)


def register_blueprints(flask_app):
    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(main_bp)
    flask_app.register_blueprint(birthdays_bp)


app = create_app()

if __name__ == "__main__":
    app.run(debug=False)
