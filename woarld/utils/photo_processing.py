import numpy as np
from PIL import Image
from skimage import morphology
from skimage.filters import threshold_adaptive
from skimage.transform import resize

THRESHOLD_VALUE = 200
PARAMETERS_BEGIN_IN = 0.5
PHOTO_WIDTH, PHOTO_HEIGHT = (592, 790)

PART_OF_FULL_PHOTO = 1

BLOCK_SIZE = (
    int(PHOTO_WIDTH * PART_OF_FULL_PHOTO),
    int(((PHOTO_HEIGHT * (1 - PARAMETERS_BEGIN_IN)) * PART_OF_FULL_PHOTO))
)


class ImageProcessor(object):
    def __init__(self, image):
        self.raw_image = image

    def get_preprocessed_block(self):
        width, height = self.raw_image.size
        image = self.raw_image.crop((0, 0, width, self.get_line_y_position()))
        image = self.grayscale_and_binarize(image)
        image = resize(image, BLOCK_SIZE[::-1], anti_aliasing=True)
        image = self.get_morphed(image)
        return image

    @staticmethod
    def get_morphed(image):
        image = image.astype('uint8')
        image = morphology.binary_erosion(image)
        image = morphology.closing(image)
        return image

    def get_parameters_image(self):
        width, height = self.raw_image.size
        return self.raw_image.crop((0, self.get_line_y_position(), width, height))

    def get_line_y_position(self):
        width, height = self.raw_image.size
        return int(height * PARAMETERS_BEGIN_IN)

    def grayscale_and_binarize(self, image):
        image = image.convert('L')
        return self.threshold(np.asarray(image))

    @staticmethod
    def threshold(image):
        block_size = 11
        return threshold_adaptive(image, block_size, offset=10)


if __name__ == '__main__':
    sample_img = Image.open('test3.jpg')

    block_img = ImageProcessor(sample_img).get_preprocessed_block()
    block_img = block_img.reshape(BLOCK_SIZE[::-1])
    block_img = block_img.reshape(BLOCK_SIZE[::-1]).astype('uint8') * 255
    img = Image.fromarray(block_img)
    img.save("processed_test_block.jpg")

    parameters_img = ImageProcessor(sample_img).get_parameters_image()
    parameters_img.save("processed_test_parameters.jpg")
