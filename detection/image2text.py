import easyocr
from PIL import Image

import io

def image2text(path):
    print(path)
    image = Image.open(path)
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes = image_bytes.getvalue()
    reader = easyocr.Reader(['ru'], gpu=False)

    text = reader.readtext(image_bytes)
    result = ''

    for item in text:
        result += item[1] + " "


    if len(result) > 1 and result[-1] == " ":
        result = result[:-1]

    return result