import json

import tornado.ioloop
import tornado.web

from faces import face_to_vec, FaceError
from images import bytes_to_img

# settings
PORT = 8000


# handlers
class Face2VecHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def post(self):
        print('asd' * 10, self.request.files, self.request)
        img_bytes = self.request.files['photo'][0]['body']
        img = bytes_to_img(img_bytes)
        try:
            face_vector = face_to_vec(img)
        except FaceError:
            response = {}
        else:
            response = {"vector": face_vector.tolist()}
        self.write(json.dumps(response))


# app
def make_app():
    return tornado.web.Application([
        (r"/face2vec", Face2VecHandler),
    ])


# running script
if __name__ == '__main__':
    app = make_app()
    app.listen(PORT)
    print("Listening on port %d..." % PORT)
    tornado.ioloop.IOLoop.current().start()
