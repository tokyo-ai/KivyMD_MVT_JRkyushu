import os

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

Builder.load_file(os.path.join(os.path.dirname(__file__), 'multiplescreen.kv'))


class fscreen(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def change(self):
        theapp.screenmanager.current = 'second screen'

class secscreen(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def change(self):
        theapp.screenmanager.current = 'first screen'


class theapp(App):
    def build(self):

        self.screenmanager = ScreenManager()

        self.fscreen = fscreen()
        screen = Screen(name='first screen')
        screen.add_widget(self.fscreen)
        self.screenmanager.add_widget(screen)

        self.secscreen = secscreen()
        screen = Screen(name='second screen')
        screen.add_widget(self.secscreen)
        self.screenmanager.add_widget(screen)

        return self.screenmanager

if __name__ == "__main__":
    theapp = theapp()
    theapp.run()