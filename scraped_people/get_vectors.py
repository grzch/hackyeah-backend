import io
import json
import requests
from PIL import Image

data_filename = 'vectors.json'
vectors = {}

with open(data_filename) as f:
    existing_vectors = json.load(f)

with open('database.json') as f:
    people = json.load(f)

not_found = []

for person in people:
    if person['name'] in existing_vectors:
        continue

    img = person["local_img_url"]
    url = 'http://localhost:8000/face2vec'
    image = open(img, 'rb')
    im = Image.open(image)
    im = im.convert('RGB')

    img_byte_arr = io.BytesIO()
    im.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    data = [
        ('photo', ('photo', img_byte_arr, 'image/jpg')),
    ]
    response = requests.post(url, files=data)
    vector = response.json()
    if not vector:
        print("face not recognized for ", person["name"])
        not_found.append(person["name"])
    else:
        vector = vector['vector']
        existing_vectors[person['name']] = vector

    with open(data_filename, 'w') as outfile:
        json.dump(existing_vectors, outfile, ensure_ascii=False)
