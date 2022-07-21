from Model.doublecamerascreen import DoubleCameraModel
from ServerCommand.cmdcontroller import CommandController
from ServerCommand.command import Command
from View.doublecamerascreen import DoubleCameraScreenView
from kivy.graphics.texture import Texture

from View.multiplescreen import theapp


class DoubleCameraScreenController:
	def __init__(self, capture_model: DoubleCameraModel):
		self.capture_model = capture_model
		self.view = DoubleCameraScreenView(controller=self, model=self.capture_model)
		self._client_command = CommandController(client_host='127.0.0.1',
												 client_port=60001,
												 server_host='127.0.0.1',
												 server_port=60002,
												 timeout=0.01)

	def get_screen(self):
		return self.view

	def get_camera_status(self):
		return self.capture_model._open_camera

	def set_camera_texture(self, value: Texture):
		self.capture_model._camera_texture = value

	def start_camera(self):
		self._client_command.send_cmd_handler(Command.START_CAMERA.value)
		# self.model.start_camera()

	def save_movie(self):
		self.capture_model.save_movie()

	def stop_camera(self):
		self._client_command.send_cmd_handler(Command.STOP_CAMERA.value)

	# self.model.stop_camera()

	def start_yolo_detector(self):
		self._client_command.send_cmd_handler(Command.START_YOLO_DETECTOR.value)

	# self.model.start_yolo_detector()

	def stop_yolo_detector(self):
		self._client_command.send_cmd_handler(Command.STOP_YOLO_DETECTOR.value)
	# self.model.stop_yolo_detector()
