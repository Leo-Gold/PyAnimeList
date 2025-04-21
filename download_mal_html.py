import requests

import settings


def url_anime_list(username, status_id, filter=''):
    try:
        url = f"https://myanimelist.net/animelist/{username}"
        response = requests.get(url, params={'status': status_id, 'tag': filter})
        response.raise_for_status()
        return response
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
    return None


def main(username):
    for status in settings.STATUS_SELECTED:
        response = url_anime_list(username, status.get('id'))
        save_content(response.text, status.get('name'))


def save_content(content, name):
    settings.DATA_SOURCE_MYANIMELIST.mkdir(parents=True, exist_ok=True)

    fullfile_path = settings.DATA_SOURCE_MYANIMELIST / f'{name}.html'

    with open(fullfile_path, "w", encoding="utf-8") as f:
        f.write(content)
        print(f"Страница сохранена в {fullfile_path}")




if __name__ == "__main__":
    username = settings.MAL_USERNAME
    if not username:
        print('Не указано имя пользователя')
        exit(1)
    main(username)
