import pprint
from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime
import pandas
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from collections import defaultdict

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')
creation_date = 1920
current_date = datetime.date.today().year
delta_time = current_date - creation_date
wines = (pandas.read_excel('wine3.xlsx', sheet_name="Лист1",
                           usecols=['Категория', 'Название', 'Сорт', 'Цена', 'Картинка', 'Акция'],
                           engine='openpyxl')
         .to_json(orient="records", force_ascii=False))

wines = json.loads(wines)
wine_list = defaultdict(list)
for wine in wines:
    wine_category = wine["Категория"]
    wine_list[wine_category].append(wine)

wine_parameters = None
for wine, sad in wine_list.items():
    print(wine)
    print(sad)
    wine_parameters = wine_list[wine]
    # for asad in wine_parameters:
        # print(asad)


def year_format(year):
    year = year % 100
    if 21 > year > 4:
        return "лет"
    year = year % 10
    if year == 1:
        return "год"
    elif 1 < year < 5:
        return "года"
    return "лет"


rendered_page = template.render(
    date=delta_time,
    year=year_format(delta_time),
    wines=wines,
    wine_list=wine_list,
    wine_parameters=wine_parameters
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
