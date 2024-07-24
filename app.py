from flask import Flask
from config import Config
from extensions import db, migrate, csrf
from models import Settings

def load_settings(app):
    settings = {setting.key: setting.value for setting in Settings.query.all()}
    app.config['APP_SETTINGS'] = settings
    app.config['APP_NAME'] = settings.get('app_name', 'Default App Name')
    app.config['APP_LOGO'] = settings.get('logo', None)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    with app.app_context():
        load_settings(app)

    @app.context_processor
    def inject_settings():
        return dict(settings=app.config.get('APP_SETTINGS', {}))

    from blueprints.dashboard import dashboard_bp
    from blueprints.users import users_bp
    from blueprints.roles import roles_bp
    from blueprints.permissions import permissions_bp
    from blueprints.settings import settings_bp

    app.register_blueprint(dashboard_bp, url_prefix='/')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(roles_bp, url_prefix='/roles')
    app.register_blueprint(permissions_bp, url_prefix='/permissions')
    app.register_blueprint(settings_bp, url_prefix='/settings')

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
