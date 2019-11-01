import cv2
from Log import log
import numpy as np


class Texture:
    def __init__(self):
        self.image = None
        self.width = 0
        self.height = 0
        self.channel = 0
        self.base_size = 0
        self.side_size = 0
        self.cube_map_image = None
        pass

    def read_img(self, path):
        self.image = cv2.imread(path)
        (self.height, self.width, self.channel) = self.image.shape
        log.info('Loaded image, height = {}, width = {}.'.format(self.height, self.width))

    def split_to_cube_map(self):
        self.check_cube_size()
        self.cube_map_image = np.zeros([self.base_size, 6 * self.base_size, 3], dtype=np.uint8)
        log.info('Got base image size: {}'.format(self.base_size))
        log.info('Target image size: {}'.format(self.cube_map_image.shape))
        if self.base_size >= self.height:
            log.err('Discouraged image size, the base size {} is larger than height {}'
                    .format(self.base_size, self.height))
            return False
        self.side_size = int((self.height - self.base_size) / 2)
        log.info('Size of side area is {}'.format(self.side_size))
        if self.side_size < self.base_size / 2:
            log.warn('Size of side area is too small.')
        return True

    def convert_to_cube_map(self):
        pic1 = self.image[0:self.side_size, 0:self.width, :]
        pic1 = cv2.resize(pic1, (self.base_size, self.base_size), interpolation=cv2.INTER_CUBIC)
        pic2 = self.image[self.side_size:self.side_size + self.base_size, 0:self.base_size, :]
        pic2 = self.rotate_image(pic2, -90)
        pic3 = self.image[self.side_size:self.side_size + self.base_size, self.base_size:2 * self.base_size, :]
        pic4 = self.image[self.side_size:self.side_size + self.base_size, 2 * self.base_size:3 * self.base_size, :]
        pic4 = self.rotate_image(pic4, 90)
        pic5 = self.image[self.side_size:self.side_size + self.base_size, 3 * self.base_size:4 * self.base_size, :]
        pic5 = self.rotate_image(pic5, 180)
        pic6 = self.image[self.side_size + self.base_size:self.height, 0:self.width, :]
        pic6 = cv2.resize(pic6, (self.base_size, self.base_size), interpolation=cv2.INTER_CUBIC)
        self.cube_map_image[0:self.base_size, 0:self.base_size, :] = pic2
        self.cube_map_image[0:self.base_size, self.base_size:2 * self.base_size, :] = pic4
        self.cube_map_image[0:self.base_size, 2 * self.base_size:3 * self.base_size, :] = pic5
        self.cube_map_image[0:self.base_size, 3 * self.base_size:4 * self.base_size, :] = pic3
        self.cube_map_image[0:self.base_size, 4 * self.base_size:5 * self.base_size, :] = pic1
        self.cube_map_image[0:self.base_size, 5 * self.base_size:6 * self.base_size, :] = pic6

    def rotate_image(self, pic, angle):
        (h, w) = pic.shape[:2]
        center = (w / 2, h / 2)
        m = cv2.getRotationMatrix2D(center, angle, 1)
        rotated = cv2.warpAffine(pic, m, (w, h))
        return rotated

    def check_cube_size(self):
        log.info("Checking the size of image.")
        for i in range(15):
            base_size = 2 ** i
            if base_size * 4 > self.width:
                self.base_size = int(2 ** (i - 1))
                break

    def save_cube_map_image(self, file_name):
        cv2.imwrite(file_name, self.cube_map_image)

    def show_cube_map_image(self):
        cv2.imshow('cube map preview', self.cube_map_image)


if __name__ == "__main__":
    tex = Texture()
    tex.read_img('pics/o_bg.jpg')
    ret = tex.split_to_cube_map()
    if ret:
        tex.convert_to_cube_map()
        while True:
            tex.show_cube_map_image()
            key = cv2.waitKey(20)
            if key == 115:
                tex.save_cube_map_image('pics/starry_output.jpg')
            if key == 32:
                break
