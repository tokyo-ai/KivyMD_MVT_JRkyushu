from kivymd.app import MDApp

from Controller.doublecamerascreen import DoubleCameraScreenController
from Model.doublecamerascreen import DoubleCameraModel


class TextMVC(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = DoubleCameraModel()
        self.controller = DoubleCameraScreenController(self.model)

    def cam_size(self):
        pass

    def start_camera(self):
        self.controller.start_camera()

    def stop_camera(self):
        self.controller.stop_camera()

    def build(self):
        return self.controller.get_screen()


if __name__ == "__main__":
    app = TextMVC()
    app.run()
