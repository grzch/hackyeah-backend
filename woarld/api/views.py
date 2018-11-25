import json

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from api.serializers import ImageUploadSerializer
from shapes_classification.classificator import nn_model
from utils.math import Plane, PRISM
from utils.photo_processing import ImageProcessor
from utils.vision import MathVision


class Detect(GenericAPIView):
    serializer_class = ImageUploadSerializer

    def get_queryset(self):
        return None

    def post(self, *args, **kwargs):
        return self.get_mocked_response()
        serializer = ImageUploadSerializer(data=self.request.data)
        serializer.is_valid()
        image = serializer.validated_data['image']

        processor = ImageProcessor(image)
        block_img = processor.get_preprocessed_block()
        params_img = processor.get_parameters_image()

        # classification
        is_prism, is_pyramid = nn_model.predict_proba(block_img.reshape(1, -1))[0]

        import scipy.misc
        scipy.misc.imsave('block.jpg', block_img)
        scipy.misc.imsave('params.jpg', params_img)

        vision = MathVision()
        definitions = vision.get_definitions(params_img)
        plane = Plane(PRISM, definitions)
        response = {
            'vertices': definitions,
            'type': 'prism' if is_prism > is_pyramid else 'pyramid'
        }
        return Response(response)

    def get_mocked_response(self):
        mocked_object = {
            "nodes": [
                # podstawa dolna
                {"name": "A", "x": -5, "y": 0, "z": 0},
                {"name": "B", "x": 5, "y": 0, "z": 0},
                {"name": "C", "x": 2, "y": 4, "z": 0},
                {"name": "D", "x": -2, "y": 4, "z": 0},
                # podstawa górna
                {"name": "E", "x": -5, "y": 0, "z": 6},
                {"name": "F", "x": 5, "y": 0, "z": 6},
                {"name": "G", "x": 2, "y": 4, "z": 6},
                {"name": "H", "x": -2, "y": 4, "z": 6},
            ],
            "connections": [
                # podstawa dolna
                {"from": "A", "to": "B"},
                {"from": "B", "to": "C"},
                {"from": "C", "to": "D"},
                {"from": "D", "to": "E"},
                # podstawa górna
                {"from": "E", "to": "F"},
                {"from": "F", "to": "G"},
                {"from": "G", "to": "H"},
                {"from": "H", "to": "E"},
                # wysokości
                {"from": "A", "to": "E"},
                {"from": "B", "to": "F"},
                {"from": "C", "to": "G"},
                {"from": "D", "to": "H"},
            ]
        }
        return Response(mocked_object)


class Historical(GenericAPIView):
    def post(self, *args, **kwargs):
        serializer = ImageUploadSerializer(data=self.request.data)
        serializer.is_valid()
        image = serializer.validated_data['image']
        # DO SOMETHING WITH IMAGE

        # CASE WITH NO PERSON
        person_not_found = True
        if person_not_found:
            return Response(status=204)

        person = self.get_person_from_database(name="Emilia Plater")
        return Response(person)

    def get_person_from_database(self, name):
        data_filename = 'scraped_people/database.json'
        with open(data_filename) as f:
            people = json.load(f)

        # MOCKED NAME
        name = "Emilia Plater"

        person_found = [person for person in people if person["name"] == name]
        if person_found:
            return person_found[0]
        return None
