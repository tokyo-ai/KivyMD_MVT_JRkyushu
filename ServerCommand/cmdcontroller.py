import logging
import socket
from typing import Iterator, Optional

from ServerCommand.command import Command


class CommandController:
	def __init__(self,
				 client_host: str, client_port: int, server_host: str, server_port: int, timeout: float):
		self._client_host = client_host
		self._client_port = client_port
		self._server_host = server_host
		self._server_port = server_port
		self._time_out = timeout
		self._cmd_buf_size = 500
		self._codec = 'utf-8'
		self._command_socket = self._create_socket(
			host=self._client_host, port=self._client_port, timeout=self._time_out
		)
		self._cmd_iters = self._iterate_command()

	def __call__(self) -> Optional[Command]:
		return next(self._cmd_iters)

	def __del__(self) -> None:
		logging.info("Terminating UDP controller server")
		self._command_socket.close()


	@staticmethod
	def _create_socket(host: str, port: int, timeout: float):
		cmd_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		try:
			cmd_socket.bind((host, port))
		except OSError:
			cmd_socket.shutdown(socket.SHUT_RD)
			cmd_socket.close()
			cmd_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			pass
		cmd_socket.settimeout(timeout)
		return cmd_socket

	def _restart_socket(self, sock: socket, host: str, port: int):
		logging.info("Restarting UDP socket")
		sock.shutdown(socket.SHUT_RD)
		sock.close()
		logging.info("Shutting down UDP socket")
		return self._create_socket(host, port, self._time_out)

	def _iterate_command(self) -> Iterator[Optional[Command]]:
		while True:
			try:
				request, receive_from_addr = self._command_socket.recvfrom(self._cmd_buf_size)
				cmd = request.strip().decode(self._codec)
				if cmd is Command.START_CAMERA.value:
					yield Command.START_CAMERA
				elif cmd is Command.STOP_CAMERA.value:
					yield Command.STOP_CAMERA
				elif cmd is Command.START_YOLO_DETECTOR.value:
					yield Command.START_YOLO_DETECTOR
				elif cmd is Command.STOP_YOLO_DETECTOR.value:
					yield Command.STOP_YOLO_DETECTOR
			except OSError as err:
				self._command_socket = self._restart_socket(self._command_socket, self._local_host, self._local_port)
				yield None

	def ack_cmd_response(self, response: str):
		with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
			sock.settimeout(0.1)
			sock.sendto(response.encode("utf-8"), (self._client_host, self._client_port))

	def send_cmd_handler(self, request_cmd_value: str):
		if request_cmd_value is not None:
			self._command_socket.sendto(str(request_cmd_value).encode(self._codec),
										(self._server_host, self._server_port))



