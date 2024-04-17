import sqlite3
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
conncection = sqlite3.connect("cars.db")
cursor = conncection.cursor()

# Resets tables
cursor.execute('''DROP TABLE IF EXISTS companies''')
cursor.execute('''DROP TABLE IF EXISTS cars''')

# Creates the Cars and Companies tables
cursor.execute('''
    CREATE TABLE companies (
        id INTEGER PRIMARY KEY,
        name TEXT,
        in_pr INTEGER,
        ds_pr INTEGER,
        description TEXT)
''')

cursor.execute('''
    CREATE TABLE cars (
        id INTEGER PRIMARY KEY,
        model TEXT,
        type TEXT,
        generations INTEGER,
        years TEXT,
        in_pr BOOLEAN,
        company_id INTEGER,
        FOREIGN KEY(company_id) REFERENCES companies(id)
    )
''')

# Holds the links of the companies and models
company_links = []
model_links = []

# Lets user know the seeding has been initialized
print("Seeding Cars. Hold on to your butts...")

# retrieves car companies info
response = Request('https://www.autoevolution.com/cars/', headers={'User-agent': 'Mozilla/5.0'})
webpage = urlopen(response).read()
soup_karl = soup(webpage, 'html.parser')

# Initilizes the index used for finding company names and model amount numbers
index_num = -1
# finds the div that holds all the company info
all_cars = soup_karl.find('div', class_="container carlist clearfix")
# finds the div that holds the amount of models that have been made
production = all_cars.findAll('div', class_="col3width fl carnums")
# Finds the div that holds the company name and links
names = all_cars.findAll('div', class_="col2width fl bcol-white carman")
for detroit in names:
    # finds the element that holds the name
    companies = detroit.findAll('h5')
    # increases index by one for each company
    index_num += 1
    for company in companies:
        # grabs the company names and uppercases it
        company_list = company.text.upper()
        # finds the index of the production number so that it is assinged to the correct company
        supply = production[index_num]
        # gets all the company links
        a_tag = company.findAll('a')
        for link in a_tag:
            company_links.append(link.get('href'))
        # gets all the production numbers
        for manufacture in supply:
            # finds all the in production and out of production model numbers
            assembly = supply.findAll('b', class_="col-green2")
            not_assembly = supply.findAll('b', class_="col-red")
            # assigns production number
            for value in assembly:
                models = int(value.text)
            # assigns not in production number
            for value in not_assembly:
                discontinued = int(value.text)
        # inserts into the tables
        cursor.execute('''INSERT INTO companies (name, in_pr, ds_pr, description)
        VALUES(?, ?, ?, ?)''', (company_list, models, discontinued, None))

# commits to database
conncection.commit()

# initializes the foreign key id
id_tracker = 0
# loops throught the list to grab all the info in each company
for page in company_links:
    url = Request(page, headers={'User-agent': 'Mozilla/5.0'})
    info = urlopen(url).read()
    cars = soup(info, 'html.parser')

    # increases the number to keep track of the id, increasing for every company
    id_tracker += 1
    # finds the description text within the car page
    company_description = cars.find('div', class_="txt prodhist")
    # if there is no text in the description, it puts in the string Null for the app to interpret
    if company_description.text == "":
        description_text = "Null"
    else:
        description_text = company_description.text
    # finds the div that holds all the current and discontinued cars
    car_div = cars.find('div', class_="col2width")
    # finds the divs that holds all the current car models within the company page
    current_model = car_div.findAll('div', class_="carmod clearfix")
    # finds the divs that holds all the old car models within the company page
    discontinued_model = car_div.findAll('div', class_="carmod clearfix disc")
    # loops through that div
    for model in current_model:
        # sets the in productioni value to true
        production_boolean = True
        # finds the currently produced model generations element
        current_generations = model.findAll('b', class_="col-green2")
        # loops through current generation div and sets the boolean to true if it finds it
        for generation in current_generations:
            car_generations = int(generation.text)
        # finds the years
        years = model.findAll('span')
        for year in years:
            model_years = year.text
        # finds all the model names within the div
        model_namses = model.findAll('h4')
        # gets the name
        for text in model_namses:
            car_model_name = text.text
        # finds the car type within the div
        car_genre = model.findAll('p', class_="body")
        # get the car type
        for value in car_genre:
            car_type = value.text.capitalize()[:-1]
        # finds all the elements with the links to the models
        car_links = model.findAll('a')
        # gets the links within that element
        for link in car_links:
            model_links.append(link.get('href'))
        # inserts into the table
        cursor.execute('''INSERT INTO cars(model, type, generations, years, in_pr, company_id)
        VALUES(?, ?, ?, ?, ?, ?)''',(car_model_name, car_type, car_generations, model_years, production_boolean, id_tracker))

    for model in discontinued_model:
        # sets the in production value to false
        production_boolean = False
        # finds the generations numbers and sets it to that
        old_generation = model.findAll('b', class_="col-red")
        for generation in old_generation:
            car_generations = int(generation.text)
        # finds the years
        years = model.findAll('span')
        for year in years:
            model_years = year.text
        # finds all the model names within the div
        model_namses = model.findAll('h4')
        # gets the name
        for text in model_namses:
            car_model_name = text.text
        # finds the car type within the div
        car_genre = model.findAll('p', class_="body")
        # get the car type
        for value in car_genre:
            car_type = value.text.capitalize()[:-1]
        # finds all the elements with the links to the models
        car_links = model.findAll('a')
        # gets the links within that element
        for link in car_links:
            model_links.append(link.get('href'))
        # inserts into the table
        cursor.execute('''INSERT INTO cars(model, type, generations, years, in_pr, company_id)
        VALUES(?, ?, ?, ?, ?, ?)''',(car_model_name, car_type, car_generations, model_years, production_boolean, id_tracker))

    # puts into the company table the description with the correct id
    cursor.execute(
        '''
        UPDATE companies
        SET description = ?
        WHERE id = ?
        ''',(description_text, id_tracker)
        )

# commits to database
conncection.commit()

# lets the user know that the seeding process is now finished
print("Cars are seeded")
