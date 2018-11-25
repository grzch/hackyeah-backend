import io
import os

# Imports the Google Cloud client library
import re

from django.conf import settings
from google.cloud import vision
from google.cloud.vision import types


EQUAL_SIGN = '='
H_SIGN = 'h'
QUESTION_SIGN = '?'
DEFINITION_REGEX = r'([\D]+)[=\-_]{1}([\d?]+)'


class Vision:
    def __init__(self):
        self.image_path = None
        self.client = vision.ImageAnnotatorClient()


class MathVision(Vision):
    def __init__(self):
        super().__init__()
        self.text = None
        self.definitions = []

    def get_definitions(self, image=None, file_name=None):
        if file_name:
            self.image_path = os.path.join(settings.MEDIA_ROOT, file_name)
            # Loads the image into memory
            with io.open(self.image_path, 'rb') as image_file:
                content = image_file.read()
        else:
            imgByteArr = io.BytesIO()
            image.save(imgByteArr, format='jpeg')
            content = imgByteArr.getvalue()
        image = types.Image(content=content)
        response = self.client.document_text_detection(image=image)
        self.text = response.full_text_annotation.text
        self.parse_text()
        return self.definitions

    def parse_text(self):
        lines = self.text.splitlines()
        for line in lines:
            self.parse_definition(line)

    def parse_definition(self, text):
        text = text.replace(' ', '')
        matches = re.findall(DEFINITION_REGEX, text)
        if matches:
            for match in matches:
                if len(match) == 2:
                    key = match[0]
                    value = match[1]

                    # b instead of h
                    if key == 'b':
                        key = 'h'

                    # no C sign detected
                    if (len(key) == 1 and value.isdigit() and H_SIGN not in key.lower())\
                            or (len(key) == 2 and value == QUESTION_SIGN):
                        key += 'C'

                    self.definitions.append(
                        self.process_data(key, value)
                    )

    @staticmethod
    def process_data(key, value):
        type = None
        if len(key) == 2:
            type = 'S'
        elif len(key) == 3:
            type = 'A'
        else:
            type = key

        return {
            'vertices': list(key),
            'value': value,
            'label': key,
            'full_text': f'{key} = {value}',
            'type': type
        }
