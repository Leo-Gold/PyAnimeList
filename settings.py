import pathlib

DATA_FOLDER = pathlib.Path('./data')

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