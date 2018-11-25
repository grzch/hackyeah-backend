from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.serializers import ImageUploadSerializer
from utils.math import Plane, PRISM, PYRAMID
from utils.photo_processing import ImageProcessor
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

        vision = MathVision()
        definitions = vision.get_definitions(image)
        plane = Plane(PRISM, definitions)
        return Response(definitions)
