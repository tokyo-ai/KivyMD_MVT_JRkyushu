import io
from os import path
import cv2
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage


class DoubleCamera(Image):
    def __init__(self, **kwargs):
        super(DoubleCamera, self).__init__(**kwargs)
        self._open_camera = False
        self._texture = self.load_jpeg_texture()
        # Clock.schedule_interval(self.update, 1.0 / 30)

    def load_jpeg_texture(self):
        initial_image_path = path.join(path.dirname(__file__),
                                       'initials.jpg')
        with open(initial_image_path, 'rb') as f:
            jpg_bytes = f.read()
            with io.BytesIO(jpg_bytes) as buf:
                return CoreImage(buf, ext='jpg').texture

    def start_camera(self):
        self._open_camera = True

    def stop_camera(self):
        self._open_camera = False

    def update(self):
        if self._open_camera:
            capture0 = cv2.VideoCapture(0)
            capture1 = cv2.VideoCapture(1)
            ret0, frame0 = capture0.read()
            ret1, frame1 = capture1.read()
            frame = cv2.hconcat(frame0, frame1)
            buf = cv2.flip(frame, 0).tostring()
            texture = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self._texture = texture
        else:
            Clock.schedule_once(self.load_jpeg_texture, 0)

    @property
    def texture(self):
        return self._texture
