import os
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty

from Utility.observer import Observer
from kivy.graphics.texture import Texture


class DoubleCameraScreenView(MDScreen, Observer):
    controller = ObjectProperty()
    model = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model.add_observer(self)

    def set_camera_texture(self, value: Texture):
        self.controller.set_camera_texture(value)

    def model_is_changed(self):
        self.ids.camview.texture = self.model._camera_texture

Builder.load_file(os.path.join(os.path.dirname(__file__), "doublecamerascreen.kv"))
# Builder.load_file(os.path.join(os.path.dirname(__file__), "store.kv"))
