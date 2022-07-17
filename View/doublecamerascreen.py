import os
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty, ListProperty
from Utility.observer import Observer
from kivy.graphics.texture import Texture


class ColorTheme:
    def __init__(self,
                 font_color,
                 background_color):
        self.font_color = font_color
        self.background_color = background_color


default_color_theme = ColorTheme(font_color=[120 / 255, 120 / 255, 120 / 255, 120 / 255],
                                 background_color=[87 / 255, 87 / 255, 87 / 255, 1])

class ConfigureScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        pass

    def change_screen(self):
        pass

class DoubleCameraScreenView(MDScreen, Observer, Screen):
    controller = ObjectProperty()
    model = ObjectProperty()
    button_font_color = ListProperty(default_color_theme.font_color)
    button_background_color = ListProperty(default_color_theme.background_color)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model.add_observer(self)

    def set_camera_texture(self, value: Texture):
        self.controller.set_camera_texture(value)

    def model_is_changed(self):
        self.ids.camview.texture = self.model._camera_texture

