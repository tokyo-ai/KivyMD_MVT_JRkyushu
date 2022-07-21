from abc import ABC, abstractmethod
from enum import auto, Enum
from typing import Optional


class Command(Enum):
	START_CAMERA = auto()
	STOP_CAMERA = auto()
	START_YOLO_DETECTOR = auto()
	STOP_YOLO_DETECTOR = auto()
	SAVE_ORIGIN_IMAGE = auto()
	SAVE_DETECTED_IMAGE = auto()
	SAVE_ORIGIN_MOVIE = auto()
	SAVE_DETECTED_MOVIE = auto()

class Controller(ABC):
    @abstractmethod
    def __call__(self) -> Optional[Command]: pass
