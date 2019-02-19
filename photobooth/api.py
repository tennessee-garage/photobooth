from flask import (
    Blueprint, current_app, g, jsonify, render_template, request, session, url_for
)
import os
from picamera import PiCamera
import tempfile


bp = Blueprint('camera', __name__, url_prefix='/camera')
camera = None


def get_camera():
    global camera
    if not camera:
        camera = PiCamera()
        get_camera().resolution = (1024, 768)
    return camera


@bp.route('/snap', methods=('GET', 'POST'))
def snap():
    img_file = generate_image_path()
    get_camera().capture(img_file)

    _, img_filename = os.path.split(img_file)
    return jsonify({
        'photo_url': '/static/photos/{}'.format(img_filename),
    })


def generate_image_path():
    photos_dir = os.path.join(current_app.root_path, 'static/photos')
    (fd, filename) = tempfile.mkstemp(suffix='.jpg', dir=photos_dir)
    return filename
