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

from Model.camera.doublecamera import DoubleCamera
from Model.image.imgstorage import GUIStorageSaver
from Model.movie.moviecreator import MovieCreator
from ServerCommand.cmdcontroller import CommandController

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
        self._image_storage_path = None
        self._movie_file_name = 'screen_capture'
        self._gui_storage_saver = GUIStorageSaver(location=BACKUP_HISTORY_DIR)
        self._double_camera = None

    @property
    def camera_texture(self):
        return self._camera_texture

    def set_camera_texture(self, value: Texture):
        self._camera_texture = value
        self.notify_observers()

    def start_camera(self):
        self._camera_status = True
        self._double_camera = DoubleCamera()
        capture0, capture1 = self._double_camera.start_double_camera()
        Clock.schedule_interval(
            lambda dt: self.refresh_content_cameraon(capture0, capture1), 1 / 45.0
        )
        Clock.schedule_interval(
            lambda dt: self.save_capture_images(), 1 / 45.0
        )

        self._image_storage_path = self._gui_storage_saver._get_data_dir_path(datetime.now().strftime('%Y_%m_%d'))

        self.notify_observers()

    def stop_camera(self):
        self._camera_status = False
        self._camera_texture = self.load_jpeg_texture()
        time.sleep(0.05)
        capture0, capture1 = self._double_camera.start_double_camera()
        Clock.unschedule(
            lambda dt: self.refresh_content_cameraon(capture0, capture1))
        time.sleep(0.05)
        Clock.unschedule(
            lambda dt: self.save_capture_images())
        self.notify_observers()

    def start_yolo_detector(self):
        pass

    def stop_yolo_detector(self):
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

    def refresh_content_cameraon(self, capture0, capture1, *args):
        self._camera_bytes = self._double_camera.h_concat_frame()
        frame01 = self._camera_bytes

        buf = cv2.flip(frame01, 0)
        if self._camera_status:
            texture = Texture.create(size=(frame01.shape[1], frame01.shape[0]), colorfmt='rgb')
            texture.blit_buffer(buf.tostring(), colorfmt='bgr', bufferfmt='ubyte')
            self.set_camera_texture(texture)

    def save_capture_images(self):
        self._gui_storage_saver.save_image(time_stamp=datetime,
                                           preview_jpg=self._camera_bytes)

    def save_movie(self):
        movie_cr = MovieCreator(image_storage_path=self._image_storage_path, movie_file_name=self._movie_file_name)
        movie_cr.create_movie()

    @staticmethod
    def resize_frame(self, frame, scale_percent=30):
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        return resized
