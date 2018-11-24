import numpy as np
from PIL import Image
from skimage.filters import threshold_adaptive

THRESHOLD_VALUE = 200
PARAMETERS_BEGIN_IN = 0.4
BLOCK_SIZE = (30, 40)


class ImageProcessor(object):
    def __init__(self, image):
        self.raw_image = image
        self.image = image

    def get_preprocessed_block(self):
        width, height = self.image.size
        image = self.raw_image.crop((0, 0, width, self.get_line_y_position()))
        image = image.resize(BLOCK_SIZE)
        image = self.grayscale_and_binarize(image)
        return image

    def get_parameters_image(self):
        width, height = self.image.size
        return self.image.crop((0, self.get_line_y_position(), width, height))

    def get_line_y_position(self):
        width, height = self.image.size
        return height * PARAMETERS_BEGIN_IN

    def grayscale_and_binarize(self, image):
        image = image.convert('L')
        return self.threshold(np.asarray(image))

    @staticmethod
    def threshold(image):
        block_size = 35
        return threshold_adaptive(image, block_size, offset=10)


if __name__ == '__main__':
    sample_img = Image.open('test.jpg')

    block_img = ImageProcessor(sample_img).get_preprocessed_block()
    block_img = block_img.reshape(BLOCK_SIZE)
    block_img = block_img.reshape(BLOCK_SIZE).astype('uint8') * 255
    img = Image.fromarray(block_img)
    img.save("processed_test_block.jpg")

    parameters_img = ImageProcessor(sample_img).get_parameters_image()
    parameters_img.save("processed_test_parameters.jpg")
