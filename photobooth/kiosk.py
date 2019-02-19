import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from photobooth.db import get_db

bp = Blueprint('kiosk', __name__, url_prefix='/kiosk')


@bp.route('/', methods=('GET', 'POST'))
def ready():
    return render_template('kiosk/ready.html')


@bp.route('/photo', methods=('GET', 'POST'))
def photo():
    return render_template('kiosk/photo.html')
