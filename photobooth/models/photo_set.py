import photo
import layout
import base


class PhotoSet(base.Base):
    TABLE = 'photo_set'

    def __init__(self):
        super(PhotoSet, self).__init__()

        self.layout_id = None
        self.layout = None  # Type: Layout
        self.created = None  # Type: datetime
        self.photos = None

    @classmethod
    def create(cls, layout_id):
        photo_set = PhotoSet()
        photo_set.layout_id = layout_id
        photo_set.save()

        return photo_set

    @classmethod
    def from_db(cls, set_id, layout_id, created):
        photo_set = PhotoSet()
        photo_set.obj_id = set_id
        photo_set.layout_id = layout_id
        photo_set.created = created
        return photo_set

    @classmethod
    def lookup(cls, set_id):  # Type: PhotoSet
        row = cls.db().execute(
                'SELECT id, layout_id, created FROM {} WHERE id = ?'.format(cls.TABLE), [set_id]
        ).fetchone()

        return PhotoSet.from_db(row[0], row[1], row[2])

    def update(self):
        self.db().execute(
            'UPDATE {} SET layout_id=?, created=? WHERE id = ?'.format(self.TABLE),
            (self.layout_id, self.created.isoformat(), self.obj_id)
        )
        self.db().commit()

    def insert(self):
        self.db().execute(
            'INSERT INTO {} (layout_id) VALUES (?)'.format(self.TABLE),
            (self.layout_id)
        )
        self.db().commit()

        self.reload_from_id(photo_set_id=self.get_last_insert_id())

    def reload_from_id(self, photo_set_id):
        ps = PhotoSet.lookup(photo_set_id)
        self.obj_id = ps.obj_id
        self.layout_id = ps.layout_id
        self.created = ps.created

    def get_photos(self):
        if not self.photos:
            self.photos = photo.Photo.all_from_set(self.obj_id)

        return self.photos

    def num_photos(self):
        photos = self.get_photos()
        if photos is None:
            return 0
        return len(photos)

    def needed_photos(self):
        layout = self.get_layout()
        return layout.num_photos

    def new_photo(self, file_name):
        return photo.Photo.from_set(set_id=self.obj_id, name=file_name)

    def get_layout(self):
        if not self.layout:
            self.layout = layout.Layout.lookup(self.layout_id)

        return self.layout
