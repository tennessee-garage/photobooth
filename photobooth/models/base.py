from photobooth.db import get_db
from flask import current_app


class Base(object):
    obj_id = None

    def __init__(self):
        pass

    def get_last_insert_id(self):
        value = self.db().execute('SELECT last_insert_rowid()').fetchone()
        if value is None:
            raise LookupError('Could not get last insert ID')

        return value[0]

    @classmethod
    def db(cls):
        return get_db()

    def save(self):
        with current_app.app_context():
            if self.obj_id:
                self.update()
            else:
                self.insert()

    def update(self):
        pass

    def insert(self):
        pass
