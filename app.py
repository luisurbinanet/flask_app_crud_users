from flask import Flask
from config import Config
from extensions import db, migrate, csrf

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from blueprints.users import users_bp
    from blueprints.roles import roles_bp
    from blueprints.permissions import permissions_bp
    from blueprints.settings import settings_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(roles_bp)
    app.register_blueprint(permissions_bp)
    app.register_blueprint(settings_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run()
