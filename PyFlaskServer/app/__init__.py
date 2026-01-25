# PyFlaskServer/app/__init__.py
# app/__init__.py – the app factory
from flask import Flask

def create_app():
    """
    Application factory for the PyFlaskServer project.
    This function is called by run.py to create and configure the Flask app.
    """
    app = Flask(__name__)
    # print(app.config)
    #Output:
    # Config {
    # 'DEBUG': False,
    # 'TESTING': False,
    # 'PROPAGATE_EXCEPTIONS': None,
    # 'SECRET_KEY': None,
    # 'PERMANENT_SESSION_LIFETIME': timedelta(days=31),
    # 'USE_X_SENDFILE': False,
    # 'SERVER_NAME': None,
    # 'APPLICATION_ROOT': '/',
    # 'SESSION_COOKIE_NAME': 'session',
    # 'SESSION_COOKIE_DOMAIN': None,
    # 'SESSION_COOKIE_PATH': None,
    # 'SESSION_COOKIE_HTTPONLY': True,
    # 'SESSION_COOKIE_SECURE': False,
    # 'SESSION_COOKIE_SAMESITE': None,
    # 'SESSION_REFRESH_EACH_REQUEST': True,
    # 'MAX_CONTENT_LENGTH': None,
    # 'SEND_FILE_MAX_AGE_DEFAULT': None,
    # 'TRAP_BAD_REQUEST_ERRORS': None,
    # 'TRAP_HTTP_EXCEPTIONS': False,
    # 'EXPLAIN_TEMPLATE_LOADING': False,
    # 'PREFERRED_URL_SCHEME': 'http',
    # 'TEMPLATES_AUTO_RELOAD': None,
    # 'MAX_COOKIE_SIZE': 4093
    # }
    # exit(0)

    # Load configuration from config.py (at project root)
    app.config.from_object("config")

    # print(app.config)
    # Config {
    # 'DEBUG': False,
    # 'TESTING': False,
    # 'PROPAGATE_EXCEPTIONS': None,
    # 'SECRET_KEY': None,
    # 'PERMANENT_SESSION_LIFETIME': timedelta(days=31),
    # 'USE_X_SENDFILE': False,
    # 'SERVER_NAME': None,
    # 'APPLICATION_ROOT': '/',
    
    # 'SESSION_COOKIE_NAME': 'session',
    # 'SESSION_COOKIE_DOMAIN': None,
    # 'SESSION_COOKIE_PATH': None,
    # 'SESSION_COOKIE_HTTPONLY': True,
    # 'SESSION_COOKIE_SECURE': False,
    # 'SESSION_COOKIE_SAMESITE': None,
    # 'SESSION_REFRESH_EACH_REQUEST': True,

    # 'MAX_CONTENT_LENGTH': None,
    # 'SEND_FILE_MAX_AGE_DEFAULT': None,
    # 'TRAP_BAD_REQUEST_ERRORS': None,
    # 'TRAP_HTTP_EXCEPTIONS': False,
    # 'EXPLAIN_TEMPLATE_LOADING': False,
    # 'PREFERRED_URL_SCHEME': 'http',
    # 'TEMPLATES_AUTO_RELOAD': None,
    # 'MAX_COOKIE_SIZE': 4093,

    # # Custom fields
    # 'DEBUG_MODE': True,
    # 'I2C_ADDRESS_RANGE': [
    #     8, 9, 10, 11, 12, 13, 14, 15,
    #     16, 17, 18, 19, 20, 21, 22, 23, 24
    # ],
    # 'I2C_BUS_ID': 5
    # }
    # exit(0)

    # diff
    # --- original
    # +++ modified
    # @@
    #     'MAX_COOKIE_SIZE': 4093
    # }
    # +
    # +    # Custom fields
    # +    'DEBUG_MODE': True,
    # +    'I2C_ADDRESS_RANGE': [
    # +        8, 9, 10, 11, 12, 13, 14, 15,
    # +        16, 17, 18, 19, 20, 21, 22, 23, 24
    # +    ],
    # +    'I2C_BUS_ID': 5

    # print("BEFORE registering blueprint:")
    # print(app.url_map)
    # Map([<Rule '/static/<filename>' (OPTIONS, GET, HEAD) -> static>])

    # Register blueprints (routes/endpoints)
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    # print("AFTER registering blueprint:")
    # print(app.url_map)
    # exit(0)
    # Map([<Rule '/static/<filename>' (GET, HEAD, OPTIONS) -> static>,
    # <Rule '/' (GET, HEAD, OPTIONS) -> main.index>,
    # <Rule '/previous' (GET, HEAD, OPTIONS) -> main.previous>])

    return app