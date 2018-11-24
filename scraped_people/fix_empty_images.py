import json
import os

data_filename = 'database.json'

with open(data_filename) as f:
    people = json.load(f)

without_blanks = []
to_remove = []

for person in people:
    size = os.path.getsize(person["local_img_url"])
    if size > 139:
        without_blanks.append(person)
    else:
        to_remove.append(person["local_img_url"])

with open(data_filename, 'w') as outfile:
    json.dump(without_blanks, outfile, ensure_ascii=False)

for path in to_remove:
    os.remove(path)
