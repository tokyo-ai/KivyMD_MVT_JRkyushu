import os
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.screen import MDScreen

from Utility.observer import Observer


class ConfigureScreenView(MDScreen, Observer, Screen):
    controller = ObjectProperty()
    model = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.model.add_observer(self)

    def model_is_changed(self):
        print('ConfigureScreenView model_is _changed')
        self.root.current = self.controller.get_screen()

KV = Builder.load_file(os.path.join(os.path.dirname(__file__), 'configure.kv'))
