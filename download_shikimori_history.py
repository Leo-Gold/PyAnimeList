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
    user_rates = save_or_read(user_rates_file, lambda: get_user_rates_all(user_id))
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
    url = "https://shikimori.one/api/v2/user_rates/"
    params = {
        'user_id': user_id,
        'target_type': 'Anime',
        'limit': settings.SHIKIMORI_LIMIT,
        'page': page,
    }

    for attempt in range(10):  # Попробуем несколько раз в случае ошибки
        try:
            response = requests.get(url, headers=create_headers(), params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 429:
                print(f"Получен 429 код (слишком много запросов). Попытка повторить через {2 ** attempt} секунд.")
                time.sleep(2 ** attempt)  # Экспоненциальная задержка: 1, 2, 4, 8, 16 секунд и т.д.
            else:
                print(f"HTTP ошибка: {http_err}")
                break
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")
            break

    return []

def get_user_rates_all(user_id):
    list_result = []
    second_request_count = 0
    minute_request_count = 0
    second_start_time = time.time()
    minute_start_time = time.time()

    page = 1
    while True:
        list_objects = get_user_rates(user_id, page)
        if not list_objects:
            break

        list_result.extend(list_objects)
        page += 1

        second_request_count += 1
        minute_request_count += 1

        if second_request_count >= 5:
            elapsed = time.time() - second_start_time
            if elapsed < 1:
                time.sleep(1 - elapsed)
            second_start_time = time.time()
            second_request_count = 0

        if minute_request_count >= 90:
            elapsed = time.time() - minute_start_time
            if elapsed < 60:
                time.sleep(60 - elapsed)
            minute_start_time = time.time()
            minute_request_count = 0

        print(page)

    return list_result

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
