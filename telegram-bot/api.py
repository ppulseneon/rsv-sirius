import json

import requests

AUTH_URL = 'http://172.16.0.151:8000'
MAIN_URL = 'http://172.16.0.151:8011'

def register(telegram_id):
    try:
        data = {
            "first_name": "string",
            "last_name": "string",
            "patronymic": "string",
            "email": str(telegram_id),
            "role": "client",
            "photo": "string"
        }

        response = requests.post(f'{AUTH_URL}/auth/registration', json=data)

        confirm_data = {
            "email": str(telegram_id),
            "role": "client",
            "code": response.json()['user']['code']
        }

        response = requests.post(f'{AUTH_URL}/auth/registration_confirm', json=confirm_data)

        return response.json()['access_token']
    except Exception as e:
        # login
        data = {
            "email": str(telegram_id),
            "role": "client"
        }

        response = requests.post(f'{AUTH_URL}/auth/auth', json=data)

        confirm_data = {
            "email": str(telegram_id),
            "role": "client",
            "code": 111111
        }

        response = requests.post(f'{AUTH_URL}/auth/auth_check', json=confirm_data)
        return response.json()['access_token']

def uploadPhoto(user, path):
    url = 'http://79.174.80.94:8015/uploadPhoto'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {user.token}'
    }
    files = {
        'file': (path, open(path, 'rb'), 'image/jpeg')
    }
    response = requests.post(url, headers=headers, files=files)

    return response.json()['url']

def add_application(user, photo):
    url = f'{MAIN_URL}/applications/add'

    data = {
        "name_product": "product",
        "photo": photo,
        "coordinates": [
            user.longitude,
            user.latitude
        ],
        "shop_id": 0
        }

    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {user.token}'
    }

    response = requests.post(url, headers=headers, json=data)

    print(response.json())
    return response.json()

def get_applications(user):
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {user.token}'
    }

    url = f'{MAIN_URL}/applications/get_my_applications'

    response = requests.get(url, headers=headers)

    print(response.json())
    return response.json()