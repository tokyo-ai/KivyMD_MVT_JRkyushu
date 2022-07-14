import os
from os import path

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from Controller.doublecamerascreen import DoubleCameraScreenController
from Model.configure import ConfigureModel
from Model.doublecamerascreen import DoubleCameraModel
from kivy.resources import resource_add_path
from kivy.core.text import DEFAULT_FONT, LabelBase

from View.configure import ConfigureScreenView


class TextMVC(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'KivyMD_MVT_JRkyushu'
        self.camera_capture_model = DoubleCameraModel()
        self.configure_model = ConfigureModel()
        self.controller = DoubleCameraScreenController(model_camera_capture=self.camera_capture_model,
                                                       model_configure=self.configure_model)



    def to_configure(self):
        self.controller.get_screen_configure()

    def start_camera(self):
        self.controller.start_camera()

    def stop_camera(self):
        self.controller.stop_camera()

    def start_yolo_detector(self):
        self.controller.start_yolo_detector()

    def stop_yolo_detector(self):
        self.controller.stop_yolo_detector()

    def save_movie(self):
        self.controller.save_movie()

    def build(self):
        return self.controller.get_screen()


if __name__ == "__main__":
    # Add Japanese font
    resource_add_path(path.join(path.dirname(__file__), "Fonts"))
    LabelBase.register(DEFAULT_FONT, 'BIZ-UDGothicB.ttc')

    app = TextMVC()
    app.run()
