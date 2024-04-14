import csv
import os
import re
from datetime import datetime
from multiprocessing import Pool

import torch

from detection.detection import detect_parts
from detection.image2text import image2text
from categories.determinant import get_category

path = 'sochi_xakaton'
category_model = 'categories/model_submit.pkl'
model = torch.hub.load('detection\yolov5', 'custom', path='best.pt', source='local')

def format_result(path, parts: dict):
    filename = path.split('/')[-1]

    name = parts.get('1.0', "неопределен")
    category = get_category(category_model, name)

    if name == 'неопределен':
        name = parts.get('2.0', "неопределен")
        category = get_category(category_model, name)

    first_price = parts.get('0.0', "100")
    last_price = parts.get('3.0', "0")

    if first_price == '':
        first_price = '100'
    if last_price == '':
        last_price = '0'

    if last_price == '00':
        last_price = '0'

    price = f'{first_price}.{last_price}'
    price = re.sub(r'[^\d\.]', '', price)

    result = f'{filename};{category};{price}'
    return result

def detect_image(path):
    parts = detect_parts(model, f'{path}')
    for key, image in parts.items():
        text = image2text(image)
        parts[key] = text

    return format_result(path, parts)


if __name__ == '__main__':
    result_filename = 'result.csv'
    dir = '/tests/'

    files = os.listdir(dir)
    i = 0
    with open('result night.csv', 'w+', encoding='utf-8') as f:
        f.write('Наименование файла;Категория продукта;Цена\n')
        for file in files:
            i+=1
            now = datetime.now()
            result = detect_image(f'{dir}{file}')
            print(datetime.now() - now)
            print(result)
            f.write(result + '\n')
            print('записано i')

# multi thread
'''
if __name__ == '__main__':
    result_filename = 'result.csv'
    dir = '/tests/'

    files = os.listdir(dir)
    pool = Pool(10)

    processed_images = pool.map(detect_image, files)
    with open('processed_images.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for image_path, processed_image in zip(files, processed_images):
            writer.writerow([image_path, processed_image])

    pool.close()
    pool.join()
'''

print('конец')