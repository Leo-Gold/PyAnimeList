import json

import requests
from bs4 import BeautifulSoup

import settings


def url_anime_list(username, status_id, filter=''):
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
    name = input('Введите ваш ник а My Anime List: ')
    for status in settings.STATUS_SELECTED:
        if status.get('name') != 'Plan to Watch':
            get_content(name, status.get('id'))
    pass


def get_content(name, status):
    result = []
    html_content = url_anime_list(name, status).text
    soup = BeautifulSoup(html_content, 'lxml')
    div = soup.find('div', id='list_surround')
    arr_tables = div.find_all('table')
    for tables in arr_tables:
        for data_td in settings.HTML_TAG_TD:
            row = tables.find_all('td', class_=data_td.get('class'))
            if row:
                result.append(row)
    return result


if __name__ == "__main__":
    main()
