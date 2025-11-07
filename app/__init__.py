from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'change-me-later'

    # register routes
    from .routes import bp as main_bp  # import the blueprint object 'bp' from routes.py in this package and alias it as main_bp
    app.register_blueprint(main_bp)

    return app