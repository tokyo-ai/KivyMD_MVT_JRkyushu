import os
from datetime import datetime
import cv2


class GUIStorageSaver:

    def __init__(self,
                 location: str,
                 basename: str):
        self._location = location
        self._baseName = basename

    def save_image(self,
                   time_stamp: datetime,
                   action_name: str,
                   preview_jpg: bytes):
        data_dir = self._get_data_dir_path(datatime_string=time_stamp.now().strftime('%Y_%m_%d_%H'))
        os.makedirs(data_dir, exist_ok=True)

        preview_file_name = f'{time_stamp.now().strftime("%Y{0}%m{1}%d{2}_%H{3}%M{4}%S{5}").format(*"YMDHMS")}_{action_name}.jpg'
        self._save_preview(parent_dir=data_dir,
                           file_name=preview_file_name,
                           preview_data=preview_jpg)

    def _get_data_dir_path(self, datatime_string: str):
        return os.path.join(self._location, datatime_string)

    @staticmethod
    def _save_preview(parent_dir: str,
                      file_name: str,
                      preview_data: bytes):
        if preview_data is not None:
            cv2.imwrite(os.path.join(parent_dir, file_name), preview_data)

