from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from api.serializers import ImageUploadSerializer
from shapes_classification.classificator import nn_model
from utils.faces_library import faces_library
from utils.math import Plane, PRISM, PYRAMID
from utils.photo_processing import ImageProcessor
from utils.photo_translator import photo_translator
from utils.vision import MathVision


class Detect(GenericAPIView):
    serializer_class = ImageUploadSerializer

    def get_queryset(self):
        return None

    def post(self, *args, **kwargs):
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
        block_type = PRISM if is_prism > is_pyramid else PYRAMID
        plane = Plane(block_type, definitions)

        nodes = []
        for label, v in plane.vertices.items():
            nodes.append({
                'name': label,
                'x': v.x,
                'y': v.y,
                'z': v.z,
            })
        response = {
            'nodes': nodes,
            'connections': plane.parsed_connections,
            'angle': plane.angle_to_find
        }
        return Response(response)

    def get_mocked_response(self):
        mocked_object = {
            "nodes": [
                {
                    "name": "A",
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                {
                    "name": "B",
                    "x": 20.0,
                    "y": 0,
                    "z": 0
                },
                {
                    "name": "C",
                    "x": 20.0,
                    "y": 10.0,
                    "z": 0
                },
                {
                    "name": "D",
                    "x": 0.0,
                    "y": 10.0,
                    "z": 0
                },
                {
                    "name": "E",
                    "x": 10.0,
                    "y": 5.0,
                    "z": 34.0
                }
            ],
            "connections": [
                {
                    "from": "A",
                    "to": "B"
                },
                {
                    "from": "C",
                    "to": "E"
                },
                {
                    "from": "B",
                    "to": "E"
                },
                {
                    "from": "B",
                    "to": "C"
                },
                {
                    "from": "D",
                    "to": "E"
                },
                {
                    "from": "A",
                    "to": "E"
                }
            ],
            "angle": [
                "E",
                "D",
                "B"
            ]
        }
        return Response(mocked_object)


class Historical(GenericAPIView):
    def post(self, *args, **kwargs):
        serializer = ImageUploadSerializer(data=self.request.data)
        serializer.is_valid()
        image = serializer.validated_data['image']

        # DO SOMETHING WITH IMAGE
        person = faces_library.get_person(image)

        # CASE WITH NO PERSON
        if person is None:
            return Response(status=204)

        # OK
        return Response(person)


class Translate(GenericAPIView):
    def post(self, *args, **kwargs):
        serializer = ImageUploadSerializer(data=self.request.data)
        serializer.is_valid()
        image = serializer.validated_data['image']

        labels = photo_translator.label_image(image)
        translations = photo_translator.translate_labels(labels)

        return Response(translations)
