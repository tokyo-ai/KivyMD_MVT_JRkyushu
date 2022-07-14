import multiprocessing as mp
from Model.doublecamerascreen import DoubleCameraModel
from View.doublecamerascreen import DoubleCameraScreenView
from kivy.graphics.texture import Texture


class DoubleCameraScreenController:
    def __init__(self, model: DoubleCameraModel):
        self.model = model
        self.view = DoubleCameraScreenView(controller=self, model=self.model)

    def get_screen(self):
        return self.view

    def get_screen_configure(self):
        return self.view.children['configure']

    def get_camera_status(self):
        return self.model._open_camera

    def set_camera_texture(self, value: Texture):
        self.model._camera_texture = value

    def start_camera(self):
        self.model.start_camera()

    def save_movie(self):
        self.model.save_movie()

    def stop_camera(self):
        self.model.stop_camera()

    def start_yolo_detector(self):
        self.model.start_yolo_detector()

    def stop_yolo_detector(self):
        self.model.stop_yolo_detector()