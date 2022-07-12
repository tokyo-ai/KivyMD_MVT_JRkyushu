import imutils as imutils
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
        Clock.schedule_interval(
            lambda dt: self.refresh_content(), 1 / 30
        )

    @property
    def camera_texture(self):
        return self._camera_texture

    def set_camera_texture(self, value: Texture):
        self._camera_texture = value
        self.notify_observers()

    def start_camera(self):
        self._camera_status = True
        self.notify_observers()

    def stop_camera(self):
        self._camera_status = False
        self._camera_texture = self.load_jpeg_texture()
        Clock.unschedule(
            lambda dt: self.refresh_content())
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

    def zip_image(self, frame, comp_ratio):
        pass

    def refresh_content(self):
        if self._camera_status:
            capture0 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not capture0.isOpened():
                raise ValueError("Failed to open camera device: 0")
                return
            ret0, frame = capture0.read()
            buf = cv2.flip(frame, 0)
            # frame = imutils.resize(frame, width=400)
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf.tostring())
            # texture.blit_buffer(buf.tostring(), colorfmt='bgr', bufferfmt='ubyte')
            self.set_camera_texture(texture)
        else:
            pass
