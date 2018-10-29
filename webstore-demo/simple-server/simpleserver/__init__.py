import os

from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # A flask secret key.
        SECRET_KEY='simpleserver'
    )


    if test_config is None:
        # Load the instance config, if it exists, when not testing.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in.
        app.config.update(test_config)

    # Ensure the instance folder exists.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'


    # Apply the blueprints to the app.
    from simpleserver import server
    app.register_blueprint(server.bp)

    # Make url_for('index') == url_for('server.index').
    app.add_url_rule('/', endpoint='index')

    return app
