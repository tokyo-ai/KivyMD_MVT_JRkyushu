from abc import abstractmethod

from kivy.graphics.texture import Texture
from kivy.properties import ObjectProperty, BooleanProperty, Clock
from kivy.uix.widget import Widget
from os import path
from kivy.core.image import Image as CoreImage
import io
import cv2


class DoubleCameraModel(Widget):
    _camera_texture = ObjectProperty(None)
    _camera_status = BooleanProperty(False)

    def __init__(self):
        self._camera_texture = self.load_jpeg_texture()
        self._camera_status = False
        self._observers = []

    @property
    def camera_texture(self):
        return self._camera_texture

    def set_camera_texture(self, value: Texture):
        self._camera_texture = value
        self.notify_observers()

    def start_camera(self):
        self._camera_status = True
        capture0 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        Clock.schedule_interval(
            lambda dt: self.refresh_content_cameraon(capture0), 1 / 45.0
        )
        self.notify_observers()

    def stop_camera(self):
        self._camera_status = False
        self._camera_texture = self.load_jpeg_texture()
        capture0 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        Clock.unschedule(
            lambda dt: self.refresh_content_cameraon(capture0))
        capture0.release()
        self.notify_observers()

    def start_yolo_detector(self):
        pass

    def start_yolo_detector(self):
        pass

    def cam_size(self):
        pass

    def add_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self):
        for x in self._observers:
            x.model_is_changed()

    def load_jpeg_texture(self):
        initial_image_path = path.join(path.dirname(__file__),
                                       'initials.jpg')
        with open(initial_image_path, 'rb') as f:
            jpg_bytes = f.read()
            with io.BytesIO(jpg_bytes) as buf:
                texture = CoreImage(buf, ext='jpg').texture
                return texture

    def refresh_content_cameraon(self, capture0, *args):
        if capture0 is None or not capture0.isOpened():
            capture0 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        ret0, frame0 = capture0.read()
        # frame_resize = self.resize_frame(frame0, 30)
        buf = cv2.flip(frame0, 0)
        texture = Texture.create(size=(frame0.shape[1], frame0.shape[0]), colorfmt='rgb')
        texture.blit_buffer(buf.tostring(), colorfmt='bgr', bufferfmt='ubyte')
        self.set_camera_texture(texture)

    @abstractmethod
    def resize_frame(self, frame, scale_percent=30):
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
