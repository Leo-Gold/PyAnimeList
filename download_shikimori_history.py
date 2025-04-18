import json

import requests

import settings

def main():
    userInfo = get_user_info()

    pass


def get_user_info():
    response = None
    username = input('Введите ваш ник на ShikiMori: ')

    try:
        url = f"https://shikimori.one/api/users/{username}/info"

        response = requests.get(url,
                                headers={'User-Agent': 'Api Test',
                                         'grant_type': 'authorization_code',
                                         'client_id': settings.SHIKIMORI_CLIENT_ID,
                                         'client_secret': settings.SHIKIMORI_CLIENT_SECRET,
                                         'code':'AUTORIZATION_CODE',
                                         'redirect_uri':'urn:ietf:wg:oauth:2.0:oob'}
                                )
        response.raise_for_status()
        return response.json()
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


if __name__ == "__main__":
    main()
