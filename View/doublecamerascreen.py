import os
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty
from Utility.observer import Observer
from kivy.graphics.texture import Texture
from kivy.uix.tabbedpanel import TabbedPanel


class ConfigureScreen(Screen):
    pass


class CaptureScreen(Screen):
    pass


class DoubleCameraScreenView(MDScreen, Observer, TabbedPanel):
    controller = ObjectProperty()
    model = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model.add_observer(self)

    def build(self):
       pass

    def set_camera_texture(self, value: Texture):
        self.controller.set_camera_texture(value)

    def model_is_changed(self):
        self.ids.camview.texture = self.model._camera_texture



class ApplicationUIManager(ScreenManager):
    pass

Builder.load_file(os.path.join(os.path.dirname(__file__), "doublecamerascreen.kv"))
# kv = Builder.load_file(os.path.join(os.path.dirname(__file__), "newtrial.kv"))