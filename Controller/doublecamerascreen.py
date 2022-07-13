import multiprocessing as mp

from kivy.uix.screenmanager import ScreenManager, Screen

from Model.doublecamerascreen import DoubleCameraModel
from View.doublecamerascreen import DoubleCameraScreenView, ConfigureScreen
from kivy.graphics.texture import Texture


class DoubleCameraScreenController:
    def __init__(self, model: DoubleCameraModel):
        self.model = model
        self.view = DoubleCameraScreenView(controller=self, model=self.model)

    def get_screen(self):
        self.screenmanager = ScreenManager()

        self.capturescreen = DoubleCameraScreenView()
        screen = Screen(name='capture screen')
        screen.add_widget(self.capturescreen)
        self.screenmanager.add_widget(screen)

        self.configurescreen = ConfigureScreen()
        screen = Screen(name='congifure screen')
        screen.add_widget(self.configurescreen)
        self.screenmanager.add_widget(screen)

        return self.screenmanager
        # return self.theapp.view

    def get_camera_status(self):
        return self.model._open_camera

    def set_camera_texture(self, value: Texture):
        self.model._camera_texture = value

    def start_camera(self):
        self.model.start_camera()
        self.model.start_camera_save()

    def stop_camera(self):
        self.model.stop_camera()

    def start_yolo_detector(self):
        self.model.start_yolo_detector()

    def stop_yolo_detector(self):
        self.model.stop_yolo_detector()