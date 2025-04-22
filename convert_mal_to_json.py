import json

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
    div = soup.find('div', id='list_surround')

    for table in div.find_all('table'):
        for tr in table.find_all('tr'):
            for td_class in settings.HTML_TAG_TD:
                for td in tr.find_all('td', class_=td_class.get('class')):
                    # пытаюсь получить массив ячеек, для их дальнейшей обработки
                    print(type(td))







if __name__ == "__main__":
    main()
