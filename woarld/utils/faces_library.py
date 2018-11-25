import io
import json

import numpy as np
import requests


class FacesLibrary:

    def __init__(self):
        with open("../scraped_people/database.json", "r") as f:
            meta = json.load(f)
            self.people_meta = {person['name']: person for person in meta}

        self.names_list = []
        with open("../scraped_people/vectors.json", "r") as f:
            faces = json.load(f)
            vectors = []
            for name, vector in faces.items():
                self.names_list.append(name)
                vectors.append(vector)
            self.faces_matrix = np.array(vectors)

    def get_person(self, image):
        url = "http://localhost:9000/face2vec"

        # img_byte_arr = io.BytesIO()
        # image.save(img_byte_arr, format='PNG')
        # img_byte_arr = img_byte_arr.getvalue()

        img_byte_arr = image

        data = [
            ('photo', ('photo', img_byte_arr, 'image/jpg')),
        ]
        vector = requests.post(url, files=data).json().get("vector")
        if vector:
            _, idx = self.nearest_vector(self.faces_matrix, vector)
            return self.people_meta[self.names_list[idx]]

    @staticmethod
    def nearest_vector(X, y):
        diff = X - y
        dists = np.square(np.einsum('ij,ij->i', diff, diff))
        idx = np.argmin(dists)
        return X[idx], idx


faces_library = FacesLibrary()