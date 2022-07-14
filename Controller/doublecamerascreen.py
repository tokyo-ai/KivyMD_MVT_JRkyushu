import multiprocessing as mp

from kivy.uix.screenmanager import ScreenManager

from Model.configure import ConfigureModel
from Model.doublecamerascreen import DoubleCameraModel
from View.configure import ConfigureScreenView
from View.doublecamerascreen import DoubleCameraScreenView
from kivy.graphics.texture import Texture


class DoubleCameraScreenController:
    def __init__(self, model_camera_capture: DoubleCameraModel, model_configure: ConfigureModel):
        self.camera_capture_model = model_camera_capture
        self.configure_model = model_configure
        self.camera_capture_view = DoubleCameraScreenView(controller=self, model=self.camera_capture_model)
        self.configure_view = ConfigureScreenView(controller=self, model=self.configure_model)

    def get_screen(self):
        return self.camera_capture_view

    def to_screenmanager(self):
        self.controller.get_screen_manager()

    def get_screen_configure(self):
        return self.configure_view

    def get_camera_status(self):
        return self.camera_capture_model._open_camera

    def set_camera_texture(self, value: Texture):
        self.camera_capture_model._camera_texture = value

    def start_camera(self):
        self.camera_capture_model.start_camera()

    def save_movie(self):
        self.camera_capture_model.save_movie()

    def stop_camera(self):
        self.camera_capture_model.stop_camera()

    def start_yolo_detector(self):
        self.camera_capture_model.start_yolo_detector()

    def stop_yolo_detector(self):
        self.camera_capture_model.stop_yolo_detector()