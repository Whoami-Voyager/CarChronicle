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
        years TEXT,
        engine TEXT,
        country TEXT,
        in_pr BOOLEAN,
        description TEXT)
''')

company_links = []
model_links = []

print("Seeding Cars. Hold on to your butts...")

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

index_tracker = -1
for page in company_links:
    url = Request(page, headers={'User-agent': 'Mozilla/5.0'})
    info = urlopen(url).read()
    cars = soup(info, 'html.parser')

    index_tracker += 1
    car_div = cars.find('div', class_="carmodels col23width clearfix")
    model_name = car_div.findAll('div', class_="col2width bcol-white fl")
    model_generation = car_div.findAll('div', class_="col3width fl")
    for model in model_generation:
        generations = model.findAll('b', class_="col-green2")
        years = model.findAll('span')
        model_namses = model_name[index_tracker]
        print(model_namses)
        for generation in generations:
            if generations:
                car_generations = int(generation.text)
            else:
                car_generations = None
        for year in years:
            model_years = year.text
        model_catalog = model_namses.findAll('h4')
        for aluminum in model_catalog:
            pass


        

    # car_info = cars.findAll('div', class_="col2width bcol-white fl")
    # for car in car_info:
    #     ca_tag = car.findAll('a')
    #     car_name = car.findAll('h4')
    #     car_type = car.findAll('p', class_='body')
    #     for tag in ca_tag:
    #         model_links.append(tag.get('href'))
    #     for name in car_name:
    #         model_list = name.text
    #     for genre in car_type:
    #         model_type = genre.text
    #     cursor.execute('''INSERT INTO cars (model, type, generations, years, engine, country, description)
    #     VALUES(?, ?, ?, ?, ?, ?, ?)''', (model_list, model_type, 1, 'h', 'h', 'h', 'h' ))

    # model_years = cars.findAll('div', class_='col3width')
    # for year in model_years:
    #     production_years = year.findAll('span')
    #     for production_year in production_years:
    #         pass
    #         model_years.append(production_year.text)


print("Cars are seeded")
