from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

#init my login LoginManager
login = LoginManager()

#inits for the database stuff
db = SQLAlchemy()
migrate = Migrate(compare_type=True)

def create_app(config_class=Config):
    #init the app
    app = Flask(__name__)
    #linking our config to the app
    app.config.from_object(Config)

    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    #this is where you will be sent if you are not logged in
    login.login_view='login'

    from.blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    from .blueprints.social import bp as social_bp
    app.register_blueprint(social_bp)

    return app

    from app import routes, models
