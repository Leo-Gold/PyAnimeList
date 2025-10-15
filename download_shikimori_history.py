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
    get_user_anime_history_all(username, user_id)
    pass

## сохранение данных или чтение данных в/из файл/а
def save_or_read(file_name, fetch_function):
    if os.path.exists(file_name):
        return read_content(file_name)
    else:
        content = fetch_function()
        save_content(content, file_name)
        return content

## заголовок запроса
def create_headers():
    return {
        'User-Agent': 'Api Test',
        'grant_type': 'authorization_code',
        'client_id': settings.SHIKIMORI_CLIENT_ID,
        'client_secret': settings.SHIKIMORI_CLIENT_SECRET,
        'code': 'AUTORIZATION_CODE',
        'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob'
    }

## получение информации
def get_user_info(username):
    try:
        url = f"https://shikimori.one/api/users/{username}/info"
        response = requests.get(url, headers=create_headers())
        response.raise_for_status()
        sleep_time()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка HTTP для пользователя {username}: {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
    return {}

## получение данных с истории просмотра
def get_user_anime_history(user_id, page):
    url = f"https://shikimori.one/api/users/{user_id}/history"
    params = {
        'limit': settings.SHIKIMORI_HISTORY_LIMIT,
        'page': page,
        'target_type': 'Anime'
    }

    try:
        response = requests.get(url, headers=create_headers(), params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
        time.sleep(60)

## проход по выбранному диапозону
def get_user_anime_history_all(username, user_id):
    page_from = settings.SHIKIMORI_ANIME_HISTORY_PAGE_FROM
    page_to = settings.SHIKIMORI_ANIME_HISTORY_PAGE_TO
    path = settings.DATA_SOURCE_SHIKIMORI
    if 1 <= page_from <= page_to <= 100000:
        for page in range(page_from, page_to + 1):
            content = get_user_anime_history(user_id, page)
            if content:
                print(page)
                file_name =  path / f"{username}_anime_history_{page}.json"
                save_content(content, file_name)
                sleep_time()
            else:
                break

## ограничение количество запросов
def sleep_time():
    time.sleep(90/60)

## сохранение в файл
def save_content(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

## чтение из файла
def read_content(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return json.load(file)


if __name__ == "__main__":
    username = settings.SHIKIMORI_USERNAME

    if not username:
        print('Не указано имя пользователя')
        exit(1)

    main(username)
