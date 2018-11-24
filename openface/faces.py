import openface

# settings
FACE_PREDICTOR_PATH = '/root/openface/models/dlib/shape_predictor_68_face_landmarks.dat'
MODEL_PATH = '/root/openface/models/openface/nn4.small2.v1.t7'
IMG_DIM = 96


# exceptions
class FaceError(Exception):
    pass


# initial objects
align = openface.AlignDlib(FACE_PREDICTOR_PATH)
net = openface.TorchNeuralNet(MODEL_PATH)


# api
def face_to_vec(image):
    bounding_box = align.getLargestFaceBoundingBox(image)
    if bounding_box is None:
        raise FaceError("There is no face in the image")
    face = align.align(
        IMG_DIM, image, bounding_box,
        landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE
    )
    if face is None:
        raise FaceError("Face cannot be aligned properly")
    return net.forward(face)
