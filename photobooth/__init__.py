import os

from flask import Flask

PHOTO_RELATIVE_DIR = 'static/photos'


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'photobooth.sqlite'),
    )

    app.photo_dir = os.path.join(app.root_path, 'static/photos')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import kiosk
    app.register_blueprint(kiosk.bp)

    from . import api
    app.register_blueprint(api.bp)

    return app
