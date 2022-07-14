import logging
import os
import datetime
from typing import Optional, Tuple

import cv2
import numpy as np


class Camera:
    def __init__(
        self,
        index: int = 0,
        size: Optional[Tuple[int, int]] = None,
        fps: Optional[float] = None,
    ):
        # Open camera device
        logging.info(
            "Opening camera device file (index={index},size={size},fps={fps})".format(
                index=index, size=size, fps=fps
            )
        )
        self._cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if not self._cap.isOpened():
            raise ValueError("Failed to open camera device: {}".format(index))

        # Capture size configuration
        if size is not None:
            w, h = size
            self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
            self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

        self._size = (
            int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        )

        if (size is not None) and (size != self._size):
            logging.warning("Failed to set capture size to {}x{}".format(*size))

        # Frame rate configuration
        if fps is not None:
            self._cap.set(cv2.CAP_PROP_FPS, fps)

        self._fps = self._cap.get(cv2.CAP_PROP_FPS)

        if (fps is not None) and (fps != self._fps):
            logging.warning("Failed to set frame rate to {:.2f}fps".format(fps))

    def get(self) -> np.ndarray:
        if not self._cap.isOpened():
            raise Exception("The device is already closed")
        ret, frame = self._cap.read()
        return frame

    def __del__(self) -> None:
        if self._cap.isOpened():
            logging.info("Releasing camera device")
            self._cap.release()


if __name__ == "__main__":
    cameraInstance0 = Camera(index=0, size=None, fps=30)
    cameraInstance1 = Camera(index=1, size=None, fps=30)
    while True:
        frame0 = cameraInstance0.get()
        frame1 = cameraInstance1.get()
        dst = cv2.hconcat([frame0, frame1])
        cv2.imshow("realtime_camera_image", dst)
        dirname = os.path.join(os.getcwd(), "mergeImages")

        t_delta = datetime.timedelta(hours=9)
        JST = datetime.timezone(t_delta, "JST")
        time = datetime.datetime.now(JST).strftime("%Y%m%d%H%M%S")

        img_name = "jr_01_{}.png".format(time)

        if not os.path.exists(dirname):
            os.mkdir(dirname)

        cv2.imwrite(
            os.path.join(dirname, img_name), dst, [cv2.IMWRITE_JPEG_QUALITY, 95]
        )
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cameraInstance0.__del__()
            cameraInstance1.__del__()
