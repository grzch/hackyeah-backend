import numpy as np
from PIL import Image
from skimage.filters import threshold_adaptive

THRESHOLD_VALUE = 200


class ImageProcessor(object):
    def __init__(self, image, size=(800, 500)):
        self.image = image
        self.size = size

    def get_binarized_image(self):
        self.resize()
        return self.grayscale_and_binarize()

    def resize(self):
        self.image = self.image.resize(self.size)

    def grayscale_and_binarize(self):
        self.image = self.image.convert('L')
        return self.threshold(np.asarray(self.image))

    @staticmethod
    def threshold(image):
        block_size = 35
        return threshold_adaptive(image, block_size, offset=10)


if __name__ == '__main__':
    sample_img = Image.open('test.jpg')
    size = (500, 500)
    binarized_img = ImageProcessor(sample_img, size).get_binarized_image()
    binarized_img = binarized_img.reshape(size)
    binarized_img = binarized_img.reshape(size).astype('uint8') * 255
    img = Image.fromarray(binarized_img)
    img.save("processed_test.jpg")
