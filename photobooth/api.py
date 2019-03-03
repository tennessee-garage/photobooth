from flask import (
    Blueprint, current_app, jsonify, request
)
import os
from camera import Camera
from models.photo_set import PhotoSet


bp = Blueprint('api', __name__, url_prefix='/api')
camera = None


def get_camera():
    global camera
    if not camera:
        camera = Camera(photos_dir=current_app.photo_dir)
    return camera


@bp.route('/photo_set', methods=['POST'])
def photo_set_create():
    if 'layout_id' not in request.form:
        raise KeyError('Parameter "layout_id" is required')

    layout_id = request.form['layout_id']
    ps = PhotoSet.create(layout_id=layout_id)

    return photo_set_response(ps)


@bp.route('/photo_set/<int:set_id>', methods=['GET'])
def photo_set_lookup(set_id):
    ps = PhotoSet.lookup(set_id=set_id)

    return photo_set_response(ps)


def photo_set_response(photo_set):
    """
    Create a response for returning PhotoSet information
    :type photo_set: PhotoSet
    """
    return jsonify({
        'id': photo_set.obj_id,
        'created': photo_set.created,
        'layout_id': photo_set.layout_id,
        'num_photos': photo_set.num_photos(),
        'needed_photos': photo_set.needed_photos(),
    })


@bp.route('/photo', methods=['POST'])
def photo():
    if 'set_id' not in request.form:
        raise KeyError('Parameter "set_id" is required')

    set_id = request.form['set_id']
    photo_set = PhotoSet.lookup(set_id)
    if photo_set is None:
        raise ValueError('No set found with ID {}'.format(set_id))

    img_file = get_camera().capture()

    _, img_filename = os.path.split(img_file)
    photo = photo_set.new_photo(img_filename)
    photo.save()

    return photo_response(photo)


def photo_response(photo):
    return jsonify({
        'id': photo.obj_id,
        'set_id': photo.set_id,
        'order_num': photo.order_num,
        'created': photo.created,
        'photo_url': '/static/photos/{}'.format(photo.file_name),
    })
