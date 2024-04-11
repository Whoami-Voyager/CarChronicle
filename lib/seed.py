from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

# Send a GET request to the URL
response = Request('https://www.autoevolution.com/cars/', headers={'User-agent': 'Mozilla/5.0'})
webpage = urlopen(response).read()

import sqlite3
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
conncection = sqlite3.connect("cars.db")
cursor = conncection.cursor()

cursor.execute('''DROP TABLE IF EXISTS companies''')
cursor.execute('''DROP TABLE IF EXISTS cars''')

cursor.execute('''
    CREATE TABLE companies (
        id INTEGER PRIMARY KEY,
        name TEXT,
        in_pr INTEGER,
        ds_pr INTEGER)
''')

cursor.execute('''
    CREATE TABLE cars (
        id INTEGER PRIMARY KEY,
        model TEXT,
        type TEXT,
        generations INTEGER,
        description TEXT,
        in_pr BOOLEAN,
        country TEXT,
        engine TEXT,
        years TEXT)
''')

company_links = []
model_list = []
model_type = []
model_links = []
model_years = []

print("loading car information, please wait... a while...")

# retrieves car companies info
response = Request('https://www.autoevolution.com/cars/', headers={'User-agent': 'Mozilla/5.0'})
webpage = urlopen(response).read()
soup_karl = soup(webpage, 'html.parser')

index_num = -1
all_cars = soup_karl.find('div', class_="container carlist clearfix")
production = all_cars.findAll('div', class_="col3width fl carnums")
names = all_cars.findAll('div', class_="col2width fl bcol-white carman")
for detroit in names:
    companies = detroit.findAll('h5')
    index_num += 1
    for company in companies:
        company_list = company.text.upper()
        supply = production[index_num]
        a_tag = company.findAll('a')
        for link in a_tag:
            company_links.append(link.get('href'))
        for manufacture in supply:
            assembly = supply.findAll('b', class_="col-green2")
            not_assembly = supply.findAll('b', class_="col-red")
            for value in assembly:
                models = int(value.text)
            for value in not_assembly:
                discontinued = int(value.text)
        cursor.execute('''INSERT INTO companies (name, in_pr, ds_pr)
        VALUES(?, ?, ?)''', (company_list, models, discontinued))

conncection.commit()

# for page in company_links:
#     url = Request(page, headers={'User-agent': 'Mozilla/5.0'})
#     info = urlopen(url).read()
#     cars = soup(info, 'html.parser')

#     car_info = cars.findAll('div', class_="col2width bcol-white fl")
#     for car in car_info:
#         ca_tag = car.findAll('a')
#         car_name = car.findAll('h4')
#         car_type = car.findAll('p', class_='body')
#         for tag in ca_tag:
#             model_links.append(tag.get('href'))
#         for name in car_name:
#             model_list.append(name.text)
#         for genre in car_type:
#             model_type.append(genre.text)

#     model_years = cars.findAll('div', class_='col3width')
#     for year in model_years:
#         production_years = year.findAll('span')
#         for production_year in production_years:
#             pass
#             # model_years.append(production_year.text)

