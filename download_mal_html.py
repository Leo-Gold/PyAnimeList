import requests

import settings

def url_anime_list(username, status_id, filter=''):
    response = None
    try:
        url = f"https://myanimelist.net/animelist/{username}"
        response = requests.get(url, params={'status': status_id, 'tag': filter})
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP ошибка: {http_err} - Код статуса: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("Ошибка соединения. Проверьте соединение с интернетом.")
    except requests.exceptions.Timeout:
        print("Превышено время ожидания.")
    except requests.exceptions.RequestException as err:
        print(f"Произошла ошибка: {err}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")


def main():
    name = input('Введите ваш ник на My Anime List: ')
    for status in settings.STATUS_SELECTED:
        content = url_anime_list(name, status.get('id')).text
        save_content(content, status.get('name'))


def save_content(content, file_name):
    settings.DATA_SOURCE_MYANIMELIST.mkdir(parents=True, exist_ok=True)
    file = f"{settings.DATA_SOURCE_MYANIMELIST}/{file_name}.html"
    with open(file, "w", encoding="utf-8") as file:
        file.write(content)
        print(f"Страница сохранена как {file}")


if __name__ == "__main__":
    main()
