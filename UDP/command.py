from enum import Enum, auto


class Command(Enum):
    START_CAMERA = auto()
    STOP_CAMERA = auto()
    START_YOLO_DETECTOR = auto()
    STOP_YOLO_DETECTOR = auto()
    RESET = auto()
    SAVE_IMG = auto()
    SAVE_MOVIE = auto()
