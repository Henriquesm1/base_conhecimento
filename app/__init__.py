from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializando SQLAlchemy e Flask-Migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # Importando as rotas
    from .routes import main
    app.register_blueprint(main)

    return app
