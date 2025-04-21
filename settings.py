import os
import pathlib

from dotenv import dotenv_values

DATA_FOLDER = pathlib.Path('./data')
DATA_SOURCE_MYANIMELIST = DATA_FOLDER / 'source' / 'myanimelist'

STATUS_SELECTED = [
    {'name': 'Currently Watching', 'id': 1},
    {'name': 'Completed', 'id': 2},
    {'name': 'On Hold', 'id': 3},
    {'name': 'Dropped', 'id': 4},
    {'name': 'Plan to Watch', 'id': 6}
]

HTML_TAG_TD = [
    {'class': 'td1'},
    {'class': 'td2'},
]

config = dotenv_values(".env")
SHIKIMORI_CLIENT_ID = config.get('SHIKIMORI_CLIENT_ID')
SHIKIMORI_CLIENT_SECRET = config.get('SHIKIMORI_CLIENT_SECRET')

MAL_USERNAME = config.get("MAL_USERNAME")
SHIKIMORI_USERNAME = config.get("SHIKIMORI_USERNAME")