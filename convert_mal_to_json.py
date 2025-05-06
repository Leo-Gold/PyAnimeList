import json
from typing import List

from bs4 import BeautifulSoup

from conf import settings
from dto import AnimeInfo


def main():
    for html in settings.STATUS_SELECTED:
        name = html.get('name')
        path = settings.DATA_SOURCE_MYANIMELIST / f'{name}.html'
        content = read_file(path)
        animeinfo_list = extract_animeinfo(content, name)
        save_json(animeinfo_list)


def read_file(file_html):
    with open(file_html, 'r', encoding='utf-8') as file:
        return file.read()


def save_json(content):
    settings.DATA_JSON_MYANIMELIST.mkdir(parents=True, exist_ok=True)
    filename = settings.DATA_JSON_MYANIMELIST / "data.json"
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(content, file, ensure_ascii=False, indent=4)


def extract_animeinfo(html_content, status) -> List[AnimeInfo]:
    soup = BeautifulSoup(html_content, 'html.parser').find("div", id="list_surround")

    tables = soup.find_all('table')

    extracted_data = []

    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            for td_class in settings.HTML_TAG_TD:
                css_class = td_class.get('class')

                columns = row.find_all('td', class_=css_class)
                extracted_data = table_columns(columns, extracted_data, status)

    return extracted_data


def table_columns(columns, extracted_data, status):
    # id_anime = columns[1].find('a', class_='List_LightBox')['href'].split('selected_series_id=')[1].split('&')[0]
    # title = columns[1].find('a', class_='animetitle').get_text(strip=True)
    # scope = columns[2].find('span', class_='score-label').get_text(strip=True)
    # progress_text = columns[4].get_text(strip=True)
    #
    # if "/" in progress_text:
    #     p = progress_text.split('/')
    #     progress_current = p[0]
    #     progress_all = p[1]
    # else:
    #     progress_current = progress_text
    #     progress_all = progress_current
    #
    # date_started = None
    # date_finished = None
    # if len(columns) == 7:
    #     date_started = columns[6].get_text(strip=True)
    #     date_finished = columns[7].get_text(strip=True)
    #
    # anime_info = AnimeInfo(title=title,
    #                        id_anime=id_anime,
    #                        scope=scope,
    #                        status=status,
    #                        progress_current=progress_current,
    #                        progress_all=progress_all,
    #                        date_started=date_started,
    #                        date_finished=date_finished
    #                        )
    # extracted_data.append(anime_info)
    return extracted_data


if __name__ == "__main__":
    main()
