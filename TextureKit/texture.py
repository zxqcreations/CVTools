import cv2
from Log import log
import numpy as np


class Texture:
    def __init__(self):
        self.image = None
        self.width = 0
        self.height = 0
        self.channel = 0
        pass

    def read_img(self, path):
        self.image = cv2.imread(path)
        (self.height, self.width, self.channel) = self.image.shape
        log.info('Loaded image, height = {}, width = {}.'.format(self.height, self.width))

    def split_to_cube6(self):
        self.check_cube_size()
        pass

    def check_cube_size(self):
        log.info("Checking the size of image.")


if __name__ == "__main__":
    tex = Texture()
    tex.read_img('pics/starry_sky_space_galaxy_118132_2048x1152.jpg')
    tex.split_to_cube6()
