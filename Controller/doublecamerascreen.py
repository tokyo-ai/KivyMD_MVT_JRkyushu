from os import path
import io

import cv2

from Model.doublecamerascreen import DoubleCameraModel
from View.doublecamerascreen import DoubleCameraScreenView
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage


class DoubleCameraScreenController:
    def __init__(self, model: DoubleCameraModel):
        self.model = model
        self.view = DoubleCameraScreenView(controller=self, model=self.model)
        # Clock.schedule_interval(self.refresh_content(self), 1 / 10.0)

    def get_screen(self):
        self.refresh_content()
        return self.view

    def get_camera_status(self):
        return self.model._open_camera

    def set_camera_texture(self, value: Texture):
        self.model._camera_texture = value

    def start_camera(self):
        self.model.start_camera()
        self.refresh_content()

    def stop_camera(self):
        self.model.stop_camera()
        self.refresh_content()

    def load_jpeg_texture(self):
        initial_image_path = path.join(path.dirname(__file__),
                                       'initials.jpg')
        with open(initial_image_path, 'rb') as f:
            jpg_bytes = f.read()
            with io.BytesIO(jpg_bytes) as buf:
                texture = CoreImage(buf, ext='jpg').texture
                return texture

    def refresh_content(self):
        if self.model._open_camera:
            capture0 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not capture0.isOpened():
                raise ValueError("Failed to open camera device: 0")
                return
            capture1 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
            if not capture1.isOpened():
                raise ValueError("Failed to open camera device: 0")
                return
            ret0, frame0 = capture0.read()
            ret1, frame1 = capture1.read()
            frame = cv2.hconcat(frame0, frame1)
            buf = cv2.flip(frame, 0).tostring()
            texture = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.view.model._camera_texture = texture
        else:
            self.view.model._camera_texture = self.load_jpeg_texture()
