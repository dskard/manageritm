from flask import Flask, Blueprint

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('flask_config_production.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_pyfile(test_config)

    # register blueprints
    from manageritm.server.main import bp as main_bp
    app.register_blueprint(main_bp)

    from manageritm.server.client import bp as client_bp
    app.register_blueprint(client_bp, url_prefix='/client')

    return app
