DROP TABLE IF EXISTS layout;

CREATE TABLE layout (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,   -- machine friendly name
  label TEXT NOT NULL,  -- human friendly name
  description TEXT NOT NULL,
  num_photos INTEGER NOT NULL DEFAULT CURRENT_TIMESTAMP
);

insert into layout (id, name, label, description, num_photos)
 values (1, 'classic', 'Classic', 'Your standard 3 photo photobooth strip', 3);

DROP TABLE IF EXISTS photo_set;

CREATE TABLE photo_set (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  layout_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (layout_id) REFERENCES layout (id)
);

DROP TABLE IF EXISTS photo;

CREATE TABLE photo (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  set_id INTEGER NOT NULL,
  order_num INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  file_name TEXT NOT NULL,
  FOREIGN KEY (set_id) REFERENCES photo_set (id)
);