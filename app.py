from flask import Flask
from config import Config
from extensions import db, migrate, csrf

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from blueprints.dashboard import dashboard_bp
    from blueprints.users.views import users_bp
    from blueprints.roles.views import roles_bp
    from blueprints.permissions.views import permissions_bp
    from blueprints.settings.views import settings_bp

    app.register_blueprint(dashboard_bp, url_prefix='/')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(roles_bp, url_prefix='/roles')
    app.register_blueprint(permissions_bp, url_prefix='/permissions')
    app.register_blueprint(settings_bp, url_prefix='/settings')

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
