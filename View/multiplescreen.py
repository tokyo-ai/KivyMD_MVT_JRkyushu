import os

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.widget import Widget

Builder.load_file(os.path.join(os.path.dirname(__file__), 'multiplescreen.kv'))


class MultiConfigureScreen(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        def change(self):
            if self.manager.current == 'configure_screen':
                self.manager.current = 'camera_view_screen'
            else:
                self.manager.current = 'configure_screen'

        def build(self):
            pass

class CameraViewScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def change(self):
        if self.manager.current == 'configure_screen':
            self.manager.current = 'camera_view_screen'
        else:
            self.manager.current = 'configure_screen'


class Manager(ScreenManager):
    configure_screen = ObjectProperty(None)
    cameraview_screen = ObjectProperty(None)

class theapp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.title = 'KivyMD_MVT_JRkyushu'
        m = Manager(transition=NoTransition())
        return m

if __name__ == "__main__":
    theapp = theapp()
    theapp.run()
