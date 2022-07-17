import os

from kivy.app import App
from kivy.lang import Builder

Builder.load_file(os.path.join(os.path.dirname(__file__), 'configure.kv'))


class ConfigureScreen(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        pass

if __name__ == "__main__":
    apps = ConfigureScreen()
    apps.run()
