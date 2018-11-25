from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.serializers import ImageUploadSerializer
from utils.math import Plane, PRISM, PYRAMID
from utils.photo_processing import ImageProcessor
from utils.vision import MathVision
from shapes_classification.classificator import nn_model


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
        plane = Plane(PRISM, definitions)
        return Response(definitions)
