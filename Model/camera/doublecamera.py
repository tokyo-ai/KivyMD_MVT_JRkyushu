import datetime
import os
from typing import Optional, Tuple

import cv2

from Model.camera.singlecamera import Camera


class DoubleCamera:
    def __init__(
            self,
            index0: int = 0,
            index1: int = 1,
            size0: Optional[Tuple[int, int]] = None,
            size1: Optional[Tuple[int, int]] = None,
            fps0: Optional[float] = None,
            fps1: Optional[float] = None,
    ):
        self.cameraInstance0 = Camera(index=index0, size=size0, fps=fps0)
        self.cameraInstance1 = Camera(index=index1, size=size1, fps=fps1)

    def h_concat_frame(self):
        frame0 = self.cameraInstance0.get()
        frame1 = self.cameraInstance1.get()
        result_frame_01 = cv2.hconcat([frame0, frame1])
        return result_frame_01

    def start_double_camera(self):
        capture0 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        capture1 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        return capture0, capture1

    @classmethod
    def createDir(cls, dirname: str):
        if not os.path.exists(dirname):
            os.mkdir(dirname)

    def save_frames(self, ext: str = "png"):
        t_delta = datetime.timedelta(hours=9)
        JST = datetime.timezone(t_delta, "JST")
        time = datetime.datetime.now(JST).strftime("%Y%m%d%H%M%S")

        cameraIds = '01'
        frames = self.h_concat_frame()
        img_name = "jr_{}_{}.{}".format(cameraIds, time, ext)
        dirname = os.path.join(os.getcwd(), cameraIds)
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        cv2.imwrite(
            os.path.join(dirname, img_name),
            frames[cameraIds],
            [cv2.IMWRITE_JPEG_QUALITY, 100],
        )

    def __del__(self) -> None:
        self.cameraInstance0.__del__()
        self.cameraInstance1.__del__()

    @classmethod
    def returnCameraIndexes(cls):
        # checks the first 10 indexes.
        index = 0
        arr = []
        i = 10
        while i > 0:
            cap = cv2.VideoCapture(index)
            if cap.read()[0]:
                arr.append(index)
                cap.release()
            index += 1
            i -= 1
        return arr
