import datetime
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import argparse
import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


def load_wine_data(file):
    return (pandas.read_excel(file, sheet_name="Лист1",
                              usecols=['Категория', 'Название', 'Сорт', 'Цена', 'Картинка', 'Акция'],
                              engine='openpyxl')
            .to_dict(orient="records"))



def calculate_time_foundation():
    creation_date = 1920
    current_date = datetime.date.today().year
    delta_time = current_date - creation_date
    return delta_time


def get_year_format(year):
    year = year % 100
    if 21 > year > 4:
        return "лет"
    year = year % 10
    if year == 1:
        return "год"
    elif 1 < year < 5:
        return "года"
    return "лет"


def render_template(wines, wine_categories, delta_time):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    return template.render(date=delta_time,
                           year=get_year_format(delta_time),
                           wines=wines,
                           wine_categories=wine_categories)


def main():
    parser = argparse.ArgumentParser(prog='file_name', description='Подгружает файл с винами, на сайт')
    parser.add_argument('file', nargs='?', default="wine3.xlsx",
                        help="Введите название файла, для загрузки на сайт", type=str)
    parser_args = parser.parse_args()
    wines = load_wine_data(parser_args.file)
    wine_categories = defaultdict(list)
    for wine in wines:
        category = wine["Категория"]
        wine_categories[category].append(wine)

    rendered_page = render_template(wines, wine_categories, calculate_time_foundation())
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
