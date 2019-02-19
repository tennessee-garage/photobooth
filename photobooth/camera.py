import os
from shutil import copyfile
import tempfile

try:
    from picamera import PiCamera
    has_module = True
except ImportError:
    has_module = False


class Camera(object):
    DEFAULT_RESOLUTION = (1024, 768)
    DUMMY_IMG = 'dummy.jpg'

    camera_object = None
    photos_dir = None

    def __init__(self, photos_dir):
        if has_module:
            self.camera_object = PiCamera()
            self.camera_object.resolution = self.DEFAULT_RESOLUTION

        self.photos_dir = photos_dir

    def capture(self):
        image_path = self.generate_image_path()
        if self.camera_object:
            print("Saving to {}".format(image_path))
            self.camera_object.capture(image_path)
        else:
            # Use a dummy image if we're not on the pi
            copyfile(self.dummy_path(), image_path)

        return image_path

    def generate_image_path(self):
        (fd, file_name) = tempfile.mkstemp(dir=self.photos_dir, suffix='.jpg')
        return file_name

    def dummy_path(self):
        return os.path.join(self.photos_dir, self.DUMMY_IMG)
