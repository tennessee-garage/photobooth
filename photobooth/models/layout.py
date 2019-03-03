import base


class Layout(base.Base):
    TABLE = 'layout'

    def __init__(self):
        super(Layout, self).__init__()

        self.layout_id = None
        self.name = None
        self.label = None
        self.description = None
        self.num_photos = None

    @classmethod
    def from_db(cls, layout_id, name, label, description, num_photos):
        layout = Layout()
        layout.layout_id = layout_id
        layout.name = name
        layout.label = label
        layout.description = description
        layout.num_photos = num_photos
        return layout

    @classmethod
    def lookup(cls, layout_id):
        row = cls.db().execute(
                'SELECT id, name, label, description, num_photos FROM {} WHERE id = ?'.format(cls.TABLE),
                [layout_id]
        ).fetchone()

        return Layout.from_db(row[0], row[1], row[2], row[3], row[4])

    def update(self):
        self.db().execute(
            'UPDATE {} SET name=?, label=?, description=?, num_photos=? WHERE id = ?'.format(self.TABLE),
            (self.name, self.label, self.description, self.num_photos, self.layout_id)
        )
        self.db().commit()

    def insert(self):
        self.db().execute(
            'INSERT INTO {} (name, label, description, num_photos) VALUES (?, ?, ?, ?)'.format(self.TABLE),
            (self.name, self.label, self.description, self.num_photos)
        )
        self.db().commit()
        self.obj_id = self.get_last_insert_id()
