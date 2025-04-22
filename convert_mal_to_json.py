from bs4 import BeautifulSoup

from conf import settings


def main():
    for html in settings.STATUS_SELECTED:
        if html.get('id') == 3:
            name = html.get('name')
            path = settings.DATA_SOURCE_MYANIMELIST / f'{name}.html'
            content = read_file(path)
            get_cell(content)
    pass


def read_file(file_html):
    with open(file_html, 'r', encoding='utf-8') as file:
        return file.read()


def get_cell(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    tables = soup.find_all('table', {'border': '0', 'cellpadding': '0', 'cellspacing': '0', 'width': '100%'})

    extracted_data = []

    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if len(columns) > 1:
                title_tag = columns[1].find('a', class_='animetitle')
                score_tag = columns[2].find('span', class_='score-label')
                type_tag = columns[3]
                tags_tag = columns[5].find('span', id=lambda x: x and x.startswith('tagLinks'))

                if title_tag and score_tag and type_tag and tags_tag:
                    title = title_tag.text.strip()
                    score = score_tag.text.strip()
                    anime_type = type_tag.text.strip()
                    tags = ', '.join(tag.text for tag in tags_tag.find_all('a'))

                    extracted_data.append((title, score, anime_type, tags))

    a = 1


if __name__ == "__main__":
    main()
