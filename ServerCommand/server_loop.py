from ServerCommand.cmdcontroller import CommandController
from ServerCommand.command import Command

if __name__ == "__main__":
	commandCtrl = CommandController()
	cmds_iter = commandCtrl._cmd_iters
	for cmd in cmds_iter:
		if cmd == Command.START_CAMERA:
			self._counter.start()
		elif cmd == Command.STOP:
			self._counter.stop()
		elif cmd == Command.RESET:
			self._counter.reset()
		elif cmd == Command.SHIFT_RIGHT:
			self._im_arranger.shift_right()
		elif cmd == Command.SHIFT_LEFT:
			self._im_arranger.shift_left()
		elif cmd == Command.SHIFT_CENTER:
			self._im_arranger.shift_center()
