import io
from os import path
from kivy.core.image import Image as CoreImage
from kivy.graphics.texture import Texture
from kivy.uix.image import Image



class DoubleCameraModel:

    def __init__(self):
        self._camera_texture = self.load_jpeg_texture()
        self._open_camera = False
        self._observers = []

    @property
    def camera_texture(self):
        return self._camera_texture

    @camera_texture.setter
    def camera_texture(self, value: Texture):
        self._camera_texture = value
        self.notify_observers()

    def load_jpeg_texture(self):
        initial_image_path = path.join(path.dirname(__file__),
                                       'initials.jpg')
        with open(initial_image_path, 'rb') as f:
            jpg_bytes = f.read()
            with io.BytesIO(jpg_bytes) as buf:
                texture = CoreImage(buf, ext='jpg').texture
                return texture


    def start_camera(self):
        self._open_camera = True
        self.notify_observers()

    def stop_camera(self):
        self._open_camera = False
        self.notify_observers()

    def cam_size(self):
        pass

    def add_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self):
        for x in self._observers:
            x.model_is_changed()
