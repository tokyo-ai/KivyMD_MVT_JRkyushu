import io
import os
import time
from datetime import datetime
from os import path

import cv2
from kivy.core.image import Image as CoreImage
from kivy.graphics.texture import Texture
from kivy.properties import ObjectProperty, BooleanProperty, Clock
from kivy.uix.widget import Widget

from Model.imgstorage import GUIStorageSaver

USER_DIR = (os.environ["USERPROFILE"]
            if "USERPROFILE" in os.environ
            else os.environ["HOME"])
BACKUP_HISTORY_DIR = path.join(USER_DIR, 'Pictures', 'JRcapture_history')


class DoubleCameraModel(Widget):
    _camera_texture = ObjectProperty(None)
    _camera_status = BooleanProperty(False)

    def __init__(self):
        self._camera_texture = self.load_jpeg_texture()
        self._camera_bytes = None
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
        Clock.schedule_interval(
            lambda dt: self.save_capture_images(), 1 / 45.0
        )
        self.notify_observers()

    def stop_camera(self):
        self._camera_status = False
        self._camera_texture = self.load_jpeg_texture()
        capture0 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        Clock.unschedule(
            lambda dt: self.refresh_content_cameraon(capture0))
        time.sleep(0.05)
        Clock.unschedule(
            lambda dt: self.save_capture_images())
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
            self._camera_bytes = jpg_bytes
            with io.BytesIO(jpg_bytes) as buf:
                texture = CoreImage(buf, ext='jpg').texture
                return texture

    def refresh_content_cameraon(self, capture0, *args):
        if capture0 is None or not capture0.isOpened():
            capture0 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        ret0, frame0 = capture0.read()
        self._camera_bytes = frame0

        # Save to local storage automatically
        data_dir = os.path.join(BACKUP_HISTORY_DIR, datetime.now().strftime('%Y_%m_%d_%H'))
        os.makedirs(data_dir, exist_ok=True)
        action_name = 'capture_screen'
        preview_file_name = f'{datetime.now().strftime("%Y{0}%m{1}%d{2}_%H{3}%M{4}%S{5}").format(*"YMDHMS")}_{action_name}.jpg'
        cv2.imwrite(os.path.join(data_dir, preview_file_name), frame0)

        buf = cv2.flip(frame0, 0)
        if self._camera_status:
            texture = Texture.create(size=(frame0.shape[1], frame0.shape[0]), colorfmt='rgb')
            texture.blit_buffer(buf.tostring(), colorfmt='bgr', bufferfmt='ubyte')
            self.set_camera_texture(texture)

    def save_capture_images(self):
        gui_storage_saver = GUIStorageSaver(location=BACKUP_HISTORY_DIR,
                                            basename='localstorage')
        gui_storage_saver.save_image(time_stamp=datetime,
                                     action_name='screen_capture',
                                     preview_jpg=self._camera_bytes)

    @staticmethod
    def resize_frame(self, frame, scale_percent=30):
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        return resized
