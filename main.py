from os import path

from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton

from Controller.doublecamerascreen import DoubleCameraScreenController
from Model.doublecamerascreen import DoubleCameraModel
from kivy.resources import resource_add_path
from kivy.core.text import DEFAULT_FONT, LabelBase


class TextMVC(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'KivyMD_MVT_JRkyushu'
        self.model = DoubleCameraModel()
        self.controller = DoubleCameraScreenController(self.model)

    def cam_size(self):
        pass

    def start_camera(self):
        self.controller.start_camera()

    def stop_camera(self):
        self.controller.stop_camera()

    def start_yolo_detector(self):
        self.controller.start_yolo_detector()

    def stop_yolo_detector(self):
        self.controller.stop_yolo_detector()

    def build(self):
        self.theme_cls.primary_palette = "LightBlue"
        screen = Screen()
        screen.add_widget(
            self.controller.get_screen()
        )
        return screen


if __name__ == "__main__":
    # Add Japanese font
    resource_add_path(path.join(path.dirname(__file__), "Fonts"))
    LabelBase.register(DEFAULT_FONT, 'BIZ-UDGothicB.ttc')

    app = TextMVC()
    app.run()
