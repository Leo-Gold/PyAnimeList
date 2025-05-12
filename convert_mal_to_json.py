import json
from dataclasses import asdict
from typing import List
from bs4 import BeautifulSoup
from conf import settings
from dto import AnimeInfo
from pathlib import Path

def main():
    all_results = []
    for html in settings.STATUS_SELECTED:
        name = html.get('name')
        path = settings.DATA_SOURCE_MYANIMELIST / f'{name}.html'
        status = html.get('status')
        all_results.extend(extract_anime_info(path, status))

    if all_results:
        save_json(all_results)
    else:
        print("Информация об аниме не извлечена.")

def extract_anime_info(path: Path, status: str) -> List[AnimeInfo]:
    result = []
    try:
        with open(path, encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        rows = soup.find_all('tr')
        class_values = [entry['class'] for entry in settings.HTML_TAG_TD]

        matching_rows = [row for row in rows if row.find('td', class_=class_values)]
        for row in matching_rows:
            try:
                id_anime = row.find('a', class_='List_LightBox')['href'].split('selected_series_id=')[1].split('&')[0]
                title = row.find('a', class_='animetitle').get_text(strip=True)
                score = row.find('span', class_='score-label').get_text(strip=True)
                progress_text = row.find_all("td")[4].get_text(strip=True)

                progress_current, progress_all = (progress_text.split('/') if '/' in progress_text else
                                                  (progress_text, progress_text))

                date_started, date_finished = None, None
                if len(row.find_all("td")) == 8:
                    date_started = row.find_all("td")[6].get_text(strip=True)
                    date_finished = row.find_all("td")[7].get_text(strip=True)

                anime_info = AnimeInfo(title=title,
                                       id_anime=id_anime,
                                       score=score,
                                       status=status,
                                       progress_current=progress_current,
                                       progress_all=progress_all,
                                       date_started=date_started,
                                       date_finished=date_finished)
                result.append(anime_info)
            except Exception as e:
                print(f"ошибка: {e}")
        return result

    except FileNotFoundError:
        print(f"Файл {path} не найден.")
    except Exception as e:
        print(f"Произошла ошибка при обработке {path}: {e}")

    return result

def save_json(content: List[AnimeInfo]):
    try:
        anime_list_dicts = [asdict(anime) for anime in content]
        settings.DATA_JSON_MYANIMELIST.mkdir(parents=True, exist_ok=True)
        filename = settings.DATA_JSON_MYANIMELIST / "data.json"
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(anime_list_dicts, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Ошибка при сохранении JSON: {e}")

if __name__ == "__main__":
    main()
