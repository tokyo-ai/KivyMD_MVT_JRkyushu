from kivy.uix.screenmanager import ScreenManager

from View.configure import ConfigureScreen
from View.doublecamerascreen import DoubleCameraScreenView


class ManagerScreen(ScreenManager):
    def build(self):
        self.configure_screen = ConfigureScreen()
        self.double_camera_view_screen = DoubleCameraScreenView()
