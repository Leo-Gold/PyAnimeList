import json

import requests

from conf import settings


def main(username):
    userInfo = get_user_info(username)

    pass


def get_user_info(username):
    response = None

    try:
        url = f"https://shikimori.one/api/users/{username}/info"

        response = requests.get(url,
                                headers={'User-Agent': 'Api Test',
                                         'grant_type': 'authorization_code',
                                         'client_id': settings.SHIKIMORI_CLIENT_ID,
                                         'client_secret': settings.SHIKIMORI_CLIENT_SECRET,
                                         'code': 'AUTORIZATION_CODE',
                                         'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob'}
                                )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")


if __name__ == "__main__":
    username = settings.SHIKIMORI_USERNAME

    if not username:
        print('Не указано имя пользователя')
        exit(1)

    main(username)
