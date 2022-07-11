import os
import io
from os import path
from kivy.core.image import Image as CoreImage
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty

from Model.doublecamerascreen import DoubleCameraModel
from Utility.observer import Observer
from kivy.graphics.texture import Texture
import cv2


class DoubleCameraScreenView(MDScreen, Observer):
    controller = ObjectProperty()
    model = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model.add_observer(self)


    def set_camera_texture(self, value: Texture):
        self.controller.set_camera_texture(value)

    def load_jpeg_texture(self):
        initial_image_path = path.join(path.dirname(__file__),
                                       'initials.jpg')
        with open(initial_image_path, 'rb') as f:
            jpg_bytes = f.read()
            with io.BytesIO(jpg_bytes) as buf:
                texture = CoreImage(buf, ext='jpg').texture
                return texture

    def model_is_changed(self):
        self.ids.doublecamera.texture = self.model._camera_texture

Builder.load_file(os.path.join(os.path.dirname(__file__), "doublecamerascreen.kv"))
