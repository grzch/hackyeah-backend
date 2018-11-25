import numpy as np
from PIL import Image
from skimage import morphology, transform
from skimage.filters import threshold_otsu

THRESHOLD_VALUE = 200
PARAMETERS_BEGIN_IN = 0.5
OFFSET = 52
PHOTO_WIDTH, PHOTO_HEIGHT = (480, 640)

PART_OF_FULL_PHOTO = 1

BLOCK_SIZE = (
    int(PHOTO_WIDTH * PART_OF_FULL_PHOTO),
    int(((PHOTO_HEIGHT * (1 - PARAMETERS_BEGIN_IN)) * PART_OF_FULL_PHOTO))
)


# iphone X viewport (375, 640) vs img size: (480, 640)


class ImageProcessor(object):
    def __init__(self, image):
        self.raw_image = Image.open(image)
        self.raw_image = self.raw_image.convert('RGB')

    def get_preprocessed_block(self):
        width, height = self.raw_image.size
        # left, upper, right, and lower pixel coordinate.
        im = self.raw_image.crop((OFFSET, 0, width - OFFSET, self.get_line_y_position()))

        im = im.convert('L')
        im = np.asarray(im)
        im = transform.resize(im, (150, 150))

        threshold = threshold_otsu(im)
        im = im < threshold
        im = morphology.binary_dilation(im)
        im = transform.resize(im, (50, 50))
        return im

    def get_parameters_image(self):
        width, height = self.raw_image.size
        return self.raw_image.crop((OFFSET, self.get_line_y_position(), width - OFFSET, height))

    def get_line_y_position(self):
        width, height = self.raw_image.size
        return int(height * PARAMETERS_BEGIN_IN)


if __name__ == '__main__':
    sample_img = Image.open('test3.jpg')

    block_img = ImageProcessor(sample_img).get_preprocessed_block()
    block_img = block_img.reshape(BLOCK_SIZE[::-1])
    block_img = block_img.reshape(BLOCK_SIZE[::-1]).astype('uint8') * 255
    img = Image.fromarray(block_img)
    img.save("processed_test_block.jpg")

    parameters_img = ImageProcessor(sample_img).get_parameters_image()
    parameters_img.save("processed_test_parameters.jpg")
