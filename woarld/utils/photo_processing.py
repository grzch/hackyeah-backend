from PIL import Image


class ImageProcessor(object):
    def __init__(self, image, size=(800, 500)):
        self.image = image
        self.size = size

    def process_and_get_image(self):
        self.resize()
        self.grayscale()
        return self.image

    def resize(self):
        self.image = self.image.resize(self.size)

    def grayscale(self):
        self.image = self.image.convert("L")


if __name__ == '__main__':
    sample_img = Image.open('test.jpg')
    processed_img = ImageProcessor(sample_img, (100, 100)).process_and_get_image()
    processed_img.save("processed_test.jpg")
