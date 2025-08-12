import json
import os
import time

import requests

from conf import settings


def main(username):
    path = settings.DATA_SOURCE_SHIKIMORI
    user_info_file = path / f"{username}_info.json"
    user_info = save_or_read(user_info_file, lambda: get_user_info(username))
    user_id = user_info.get('id')

    user_rates_file = path / f"{username}_user_rate.json"
    user_rates = save_or_read(user_rates_file, lambda: get_user_rates(user_id, 1))
    print(user_rates)
    pass


def save_or_read(file_name, fetch_function):
    if os.path.exists(file_name):
        return read_content(file_name)
    else:
        content = fetch_function()
        save_content(content, file_name)
        return content


def create_headers():
    return {
        'User-Agent': 'Api Test',
        'grant_type': 'authorization_code',
        'client_id': settings.SHIKIMORI_CLIENT_ID,
        'client_secret': settings.SHIKIMORI_CLIENT_SECRET,
        'code': 'AUTORIZATION_CODE',
        'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob'
    }


def get_user_info(username):
    try:
        url = f"https://shikimori.one/api/users/{username}/info"
        response = requests.get(url, headers=create_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка HTTP для пользователя {username}: {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
    return {}


def get_user_rates(user_id, page):
    try:
        url = f"https://shikimori.one/api/v2/user_rates/"
        params = {
            'user_id': user_id,
            'target_type': 'Anime',
            'limit': settings.SHIKIMORI_LIMIT,
            '': page,
        }
        response = requests.get(url, headers=create_headers(), params=params)
        response.raise_for_status()
        result_page = json.loads(response.json())
        return result_page
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
    return []

def get_user_rates_all(user_id):
    
    pass



def save_content(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def read_content(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return json.load(file)


if __name__ == "__main__":
    username = settings.SHIKIMORI_USERNAME

    if not username:
        print('Не указано имя пользователя')
        exit(1)

    main(username)
