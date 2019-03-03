from datetime import datetime
import time

import base
import photo_set


class Photo(base.Base):
    TABLE = 'photo'

    def __init__(self):
        super(Photo, self).__init__()

        self.set_id = None
        self.order_num = None
        self.created = None  # Type: datetime
        self.file_name = None
        self.set = None  # Type: PhotoSet

    @classmethod
    def from_db(cls, photo_id, set_id, order_num, created, file_name):
        photo = Photo()
        photo.obj_id = photo_id
        photo.set_id = set_id
        photo.order_num = order_num
        photo.created = created
        photo.file_name = file_name
        return photo

    @classmethod
    def from_set(cls, set_id, name):
        photo = Photo()
        photo.set_id = set_id
        photo.file_name = name
        return photo

    def set_new_photo(self, file_name):
        self.file_name = file_name

    @classmethod
    def lookup(cls, photo_id):
        row = cls.db().execute(
                'SELECT id, set_id, order_num, created, file_name FROM {} WHERE id = ?'.format(cls.TABLE),
                [photo_id]
        ).fetchone()

        return Photo.from_db(row[0], row[1], row[2], row[3], row[4])

    @classmethod
    def all_from_set(cls, set_id):
        photos = []
        sql = 'SELECT id, set_id, order_num, created, file_name FROM {} WHERE set_id = ?'.format(cls.TABLE)
        for row in cls.db().execute(sql, [set_id]):
            photo = Photo.from_db(row[0], row[1], row[2], row[3], row[4])
            photos.append(photo)

        return photos

    def update(self):
        """
        Update a photo object.  Don't allow updating order or set_id
        :return: Photo
        """
        self.db().execute(
            'UPDATE {} SET created=?, file_name=? WHERE id = ?'.format(self.TABLE),
            (self.created.isoformat(), self.file_name, self.obj_id)
        )
        self.db().commit()

    def insert(self):
        num = self.get_next_order_num()
        self.db().execute(
            'INSERT INTO {} (set_id, order_num, file_name) VALUES (?, ?, ?)'.format(self.TABLE),
            [self.set_id, num, self.file_name]
        )
        self.db().commit()

        self.reload_from_id(photo_id=self.get_last_insert_id())

    def reload_from_id(self, photo_id):
        p = Photo.lookup(photo_id)
        self.obj_id = photo_id
        self.set_id = p.set_id
        self.order_num = p.order_num
        self.created = p.created
        self.file_name = p.file_name

    def get_next_order_num(self):
        """
        In another DB this would be handled by a stored procedure, but here we are...
        :return: int
        """
        row = self.db().execute(
            'SELECT MAX(order_num) FROM {} WHERE set_id=?'.format(self.TABLE),
            [self.set_id]
        ).fetchone()

        if row is None or row[0] is None:
            return 0
        else:
            return row[0] + 1

    def get_set(self):
        if not self.set:
            self.set = photo_set.PhotoSet.lookup(self.set_id)

        return self.set
