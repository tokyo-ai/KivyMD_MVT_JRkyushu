from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

class ColorTheme:
    def __init__(self,
                 font_color,
                 background_color):
        self.font_color = font_color
        self.background_color = background_color


default_color_theme = ColorTheme(font_color=[120 / 255, 120 / 255, 120 / 255, 120 / 255],
                                 background_color=[87 / 255, 87 / 255, 87 / 255, 1])


class CaptureScreenView(Screen):
    pass

class ConfigureScreenView(Screen):
    pass

class ProScreenManager(ScreenManager):
    pass



class MyMainApp(App):
    kv = Builder.load_file("pro_screenmanager.kv")
    def build(self):
        return self.kv


if __name__ == "__main__":
    MyMainApp().run()
