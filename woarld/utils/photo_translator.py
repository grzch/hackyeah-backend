import io

from google.cloud import translate, vision
from google.cloud.vision import types


class PhotoTranslator:
    languages = ['pl', 'de', 'es', 'fr']

    def __init__(self):
        self.vision_client = vision.ImageAnnotatorClient()
        self.translate_client = translate.Client()

    def label_image(self, image):
        img_byte_arr = image.read()

        gImage = types.Image(content=img_byte_arr)
        labels = [
            l.description
            for l in self.vision_client.label_detection(gImage).label_annotations[:2]
            if l.score > 0.8
        ]
        return labels

    def translate_labels(self, labels):
        translations = {label: {} for label in labels}
        for lang in self.languages:
            response = self.translate_client.translate(labels, target_language=lang)
            for translation in response:
                translations[translation['input']][lang] = translation['translatedText']
        return [{'en': word, **trans} for word, trans in translations.items()]


photo_translator = PhotoTranslator()
