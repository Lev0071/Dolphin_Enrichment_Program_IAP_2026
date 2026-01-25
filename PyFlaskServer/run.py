# PyFlaskServer/run.py
# run.py
from app import create_app                                      # create_app() lives in app/__init__.py
from config import DEBUG_MODE

app = create_app()

# print("START -- App dictionary")
# for name in dir(app):
#     try:
#         attr = getattr(app, name)
#         if isinstance(attr, dict):
#             print(f"\n{name} =")
#             print(attr)
#     except Exception:
#         pass
# print("END -- App dictionary")
# exit(0)
# Output:
# # ---------- Flask App Introspection Dump (Neatened for Reference) ----------

# __annotations__ = {
#     'json_provider_class': 'type[JSONProvider]',
#     'jinja_options': 'dict',
#     'test_client_class': 'type[FlaskClient] | None',
#     'test_cli_runner_class': 'type[FlaskCliRunner] | None',
#     'session_interface': 'SessionInterface'
# }

# __dict__ = {
#     'import_name': 'app',
#     '_static_folder': 'static',
#     '_static_url_path': None,
#     'template_folder': 'templates',

#     'root_path':
#         'C:\\Users\\User\\Documents\\6002ENG\\Button_arrainge Project\\dolphin_enrichment_clean\\PyFlaskServer\\app',

#     'cli': <AppGroup app>,

#     'view_functions': {
#         'static': <function Flask.__init__.<locals>.<lambda> at 0x0000024EB735D3A0>,
#         'main.index': <function index at 0x0000024EB735F4C0>,
#         'main.previous': <function previous at 0x0000024EB735F600>
#     },

#     'error_handler_spec':
#         defaultdict(<function Scaffold.__init__.<locals>.<lambda> at 0x0000024EB496C0E0>, {}),

#     'before_request_funcs': defaultdict(list, {}),
#     'after_request_funcs': defaultdict(list, {}),
#     'teardown_request_funcs': defaultdict(list, {}),

#     'template_context_processors': defaultdict(
#         list,
#         {
#             None: [<function _default_template_ctx_processor at 0x0000024EB72D4860>],
#             'main': [<function _default_template_ctx_processor at 0x0000024EB72D4860>]
#         }
#     ),

#     'url_value_preprocessors': defaultdict(list, {}),
#     'url_default_functions': defaultdict(list, {}),

#     'instance_path':
#         'C:\\Users\\User\\Documents\\6002ENG\\Button_arrainge Project\\dolphin_enrichment_clean\\PyFlaskServer\\instance',

#     'config': <Config {
#         'DEBUG': False,
#         'TESTING': False,
#         'PROPAGATE_EXCEPTIONS': None,
#         'SECRET_KEY': None,
#         'PERMANENT_SESSION_LIFETIME': timedelta(days=31),
#         'USE_X_SENDFILE': False,
#         'SERVER_NAME': None,
#         'APPLICATION_ROOT': '/',
#         'SESSION_COOKIE_NAME': 'session',
#         'SESSION_COOKIE_DOMAIN': None,
#         'SESSION_COOKIE_PATH': None,
#         'SESSION_COOKIE_HTTPONLY': True,
#         'SESSION_COOKIE_SECURE': False,
#         'SESSION_COOKIE_SAMESITE': None,
#         'SESSION_REFRESH_EACH_REQUEST': True,
#         'MAX_CONTENT_LENGTH': None,
#         'SEND_FILE_MAX_AGE_DEFAULT': None,
#         'TRAP_BAD_REQUEST_ERRORS': None,
#         'TRAP_HTTP_EXCEPTIONS': False,
#         'EXPLAIN_TEMPLATE_LOADING': False,
#         'PREFERRED_URL_SCHEME': 'http',
#         'TEMPLATES_AUTO_RELOAD': None,
#         'MAX_COOKIE_SIZE': 4093,

#         # Custom config entries
#         'DEBUG_MODE': True,
#         'I2C_ADDRESS_RANGE': [
#             8, 9, 10, 11, 12, 13, 14, 15,
#             16, 17, 18, 19, 20, 21, 22, 23, 24
#         ],
#         'I2C_BUS_ID': 5
#     }>,

#     'aborter': <werkzeug.exceptions.Aborter object at 0x0000024EB7237390>,
#     'json': <flask.json.provider.DefaultJSONProvider object at 0x0000024EB7292F90>,

#     'url_build_error_handlers': [],
#     'teardown_appcontext_funcs': [],
#     'shell_context_processors': [],

#     'blueprints': {
#         'main': <Blueprint 'main'>
#     },

#     'extensions': {},

#     'url_map': Map([
#         <Rule '/static/<filename>' (GET, OPTIONS, HEAD) -> static>,
#         <Rule '/' (GET, OPTIONS, HEAD) -> main.index>,
#         <Rule '/previous' (GET, OPTIONS, HEAD) -> main.previous>
#     ]),

#     'subdomain_matching': False,
#     '_got_first_request': False,

#     'name': 'app'
# }

# after_request_funcs =
#     defaultdict(list, {})

# before_request_funcs =
#     defaultdict(list, {})

# blueprints =
#     {'main': <Blueprint 'main'>}

# config =
#     <Config { ...same as above... }>

# default_config =
#     ImmutableDict({
#         'DEBUG': None,
#         'TESTING': False,
#         'PROPAGATE_EXCEPTIONS': None,
#         'SECRET_KEY': None,
#         'PERMANENT_SESSION_LIFETIME': timedelta(days=31),
#         'USE_X_SENDFILE': False,
#         'SERVER_NAME': None,
#         'APPLICATION_ROOT': '/',
#         'SESSION_COOKIE_NAME': 'session',
#         'SESSION_COOKIE_DOMAIN': None,
#         'SESSION_COOKIE_PATH': None,
#         'SESSION_COOKIE_HTTPONLY': True,
#         'SESSION_COOKIE_SECURE': False,
#         'SESSION_COOKIE_SAMESITE': None,
#         'SESSION_REFRESH_EACH_REQUEST': True,
#         'MAX_CONTENT_LENGTH': None,
#         'SEND_FILE_MAX_AGE_DEFAULT': None,
#         'TRAP_BAD_REQUEST_ERRORS': None,
#         'TRAP_HTTP_EXCEPTIONS': False,
#         'EXPLAIN_TEMPLATE_LOADING': False,
#         'PREFERRED_URL_SCHEME': 'http',
#         'TEMPLATES_AUTO_RELOAD': None,
#         'MAX_COOKIE_SIZE': 4093
#     })

# error_handler_spec =
#     defaultdict(<function Scaffold.__init__.<locals>.<lambda>>, {})

# extensions =
#     {}

# jinja_options =
#     {}

# teardown_request_funcs =
#     defaultdict(list, {})

# template_context_processors =
#     defaultdict(list, {
#         None: [<_default_template_ctx_processor>],
#         'main': [<_default_template_ctx_processor>]
#     })

# url_default_functions =
#     defaultdict(list, {})

# url_value_preprocessors =
#     defaultdict(list, {})

# view_functions =
# {
#     'static': <function Flask.__init__.<locals>.<lambda> at 0x0000024EB735D3A0>,
#     'main.index': <function index at 0x0000024EB735F4C0>,
#     'main.previous': <function previous at 0x0000024EB735F600>
# }

# # ---------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=DEBUG_MODE)