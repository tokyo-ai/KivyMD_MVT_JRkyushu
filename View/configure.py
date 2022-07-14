import os

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

Builder.load_file(os.path.join(os.path.dirname(__file__), 'configure.kv'))


class ConfigureScreen(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        pass


class theapp(App):
    def build(self):

        self.screenmanager = ScreenManager()
        self.configurescreen = ConfigureScreen()

        screen = Screen(name = 'first screen')

        screen.add_widget(self.configurescreen)
        self.screenmanager.add_widget(screen)


        return self.screenmanager

if __name__ == "__main__":
    theapp = theapp()
    theapp.run()
