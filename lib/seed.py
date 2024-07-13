import sqlite3
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
from alive_progress import alive_bar

# Establish a connection to the database
connection = sqlite3.connect("cars.db")
cursor = connection.cursor()

# Reset tables
cursor.execute('''DROP TABLE IF EXISTS companies''')
cursor.execute('''DROP TABLE IF EXISTS cars''')

# Create the Companies and Cars tables
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

# Inform the user that seeding has started
print("Seeding Cars. Hold on to your butts...\n")

# Retrieve car companies info
response = Request('https://www.autoevolution.com/cars/', headers={'User-agent': 'Mozilla/5.0'})
webpage = urlopen(response).read()
soup_karl = soup(webpage, 'html.parser')

# Initialize the index used for finding company names and model amount numbers
index_num = -1
# Find the div that holds all the company info
all_cars = soup_karl.find('div', class_="container carlist clearfix")
# Find the div that holds the amount of models that have been made
production = all_cars.findAll('div', class_="col3width fl carnums")
# Find the div that holds the company name and links
names = all_cars.findAll('div', class_="col2width fl bcol-white carman")
for detroit in names:
    # Find the element that holds the name
    companies = detroit.find('h5')
    # Increase index by one for each company
    index_num += 1
    # Grab the company names and uppercase them
    company_list = companies.text.upper()
    # Find the index of the production number so that it is assigned to the correct company
    supply = production[index_num]
    # Get all the company links
    a_tag = detroit.find('a')
    company_links.append(a_tag.get('href'))
    # Get all the production numbers
    for manufacture in supply:
        # Find all the in-production and out-of-production model numbers
        assembly = supply.find('b', class_="col-green2")
        not_assembly = supply.find('b', class_="col-red")
        # Assign production number
        models = int(assembly.text)
        # Assign not in production number
        discontinued = int(not_assembly.text)
    # Insert into the tables
    cursor.execute('''INSERT INTO companies (name, in_pr, ds_pr, description)
    VALUES(?, ?, ?, ?)''', (company_list, models, discontinued, None))

# Commit to database
connection.commit()

# Initialize the foreign key id
id_tracker = 0

# the alive bar that the entire seed file runs under
with alive_bar(len(company_links), bar="filling") as bar:
    # Loop through the list to grab all the info in each company
    for page in company_links:
        url = Request(page, headers={'User-agent': 'Mozilla/5.0'})
        info = urlopen(url).read()
        cars = soup(info, 'html.parser')

        # Increase the number to keep track of the id, increasing for every company
        id_tracker += 1
        # the progress bar to let people know how far along the seeding process is
        bar()
        # Find the description text within the car page
        company_description = cars.find('div', class_="txt prodhist")
        # Strip down the text
        description_text = company_description.text.strip()
        # Find the div that holds all the current and discontinued cars
        car_div = cars.find('div', class_="col2width")
        # Find the divs that hold all the current car models within the company page
        current_model = car_div.findAll('div', class_="carmod clearfix")
        # Find the divs that hold all the old car models within the company page
        discontinued_model = car_div.findAll('div', class_="carmod clearfix disc")
        # Loop through that div
        for model in current_model:
            # Set the in production value to true
            production_boolean = True
            # Find the currently produced model generations element
            current_generations = model.find('b', class_="col-green2")
            # Loop through current generation div and set the boolean to true if it finds it
            car_generations = int(current_generations.text)
            # Find the years
            years = model.findAll('span')
            for year in years:
                model_years = year.text
            # Find all the model names within the div
            model_names = model.find('h4')
            # Get the name
            car_model_name = model_names.text
            # Find the car type within the div
            car_genre = model.find('p', class_="body")
            # Get the car type
            car_type = car_genre.text.capitalize()[:-1]
            # Find all the elements with the links to the models
            car_link = model.find('a')
            # Get the links within that element
            model_links.append(car_link.get('href'))
            # Insert into the table
            cursor.execute('''INSERT INTO cars(model, type, generations, years, in_pr, company_id)
            VALUES(?, ?, ?, ?, ?, ?)''',(car_model_name, car_type, car_generations, model_years, production_boolean, id_tracker))

        for model in discontinued_model:
            # Set the in production value to false
            production_boolean = False
            # Find the generations numbers and set it to that
            old_generation = model.find('b', class_="col-red")
            car_generations = int(old_generation.text)
            # Find the years
            years = model.findAll('span')
            for year in years:
                model_years = year.text
            # Find all the model names within the div
            model_names = model.find('h4')
            # Get the name
            car_model_name = model_names.text
            # Find the car type within the div
            car_genre = model.find('p', class_="body")
            # Get the car type
            car_type = car_genre.text.capitalize()[:-1]
            # Find all the elements with the links to the models
            car_links = model.find('a')
            # Get the links within that element
            model_links.append(car_links.get('href'))
            # Insert into the table
            cursor.execute('''INSERT INTO cars(model, type, generations, years, in_pr, company_id)
            VALUES(?, ?, ?, ?, ?, ?)''',(car_model_name, car_type, car_generations, model_years, production_boolean, id_tracker))

        # Put into the company table the description with the correct id
        cursor.execute(
            '''
            UPDATE companies
            SET description = ?
            WHERE id = ?
            ''',(description_text, id_tracker)
            )
    


# Commit to database
connection.commit()

# Inform the user that the seeding process is now finished
print("\nCars are seeded")
