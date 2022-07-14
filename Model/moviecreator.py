import glob
import os
from datetime import datetime
from typing import List

import cv2
'''
https://theailearner.com/2018/10/15/creating-video-from-images-using-opencv-python/'''
path = os.getcwd()

class MovieCreator:
    def __init__(self,
                 image_storage_path: str,
                 movie_file_name: str):
        self._image_storage_path = image_storage_path
        self._move_file_name = movie_file_name

    def create_movie(self):
        img_array = []
        for filename in os.path.join(glob.glob(self._image_storage_path) , datetime.now().strftime('%Y_%m_%d')):
            img = cv2.imread(os.path.join(self._image_storage_path, filename))
            h,w,layer=img.shape
            size=(w,h)
            img_array.append(img)
        out = cv2.VideoWriter(self._movie_file_name, cv2.VideoWriter_fourcc(*'DIVX'), 15, size)   #  *'DIVX' for .avi; *'MP4V' for .mp4
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()



