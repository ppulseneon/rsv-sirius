import uuid
from datetime import datetime

import requests
import torch
from flask import Flask, jsonify, request

from categories.determinant import get_category
from detection.detection import detect_parts
from detection.image2text import image2text

app = Flask(__name__)
model = torch.hub.load('detection\yolov5', 'custom', path='best.pt', source='local')
category_model = 'categories/model.pkl'

@app.route('/')
def hello_world():
    return jsonify('Hello World!')


@app.route("/detection-nametag", methods=['POST'])
def detection():
    start_time = datetime.now()
    data = request.get_json()

    image = data['image']
    image_path = f'temp/{uuid.uuid4()}.jpg'
    p = requests.get(image)
    out = open(image_path, "wb")
    out.write(p.content)
    out.close()

    parts = detect_parts(model, image_path)
    for key, image in parts.items():
        text = image2text(image)
        name = ''

        if key == '0.0':
            first_price = text
        if key == '1.0':
            name = text
            print(name)
            category = get_category(category_model, text)
        if key == '3.0':
            last_price = text

    if first_price == '':
        first_price = -1

    if last_price == '':
        last_price = 0

    if name == '':
        if text == '':
            text = 'ошибка'
        else:
            name = text
        category = get_category(category_model, name)

    first_price = ''.join(c if c.isdigit() else ' ' for c in first_price).split()[0]
    price = f'{first_price}.{last_price}'

    result = {'status': True, 'data': {'name': name, 'category': category, 'price': price}}

    print(f'work time: {datetime.now()-start_time}')
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234)