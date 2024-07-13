import sqlite3
conncection = sqlite3.connect("cars.db")
cursor = conncection.cursor()

# The class that holds and initializes companies
class Company:

    # intializes the class with name, production numbers, and description
    def __init__(self, name, in_pr, ds_pr, description):
        self.name = name
        self.in_pr = in_pr
        self.ds_pr = ds_pr
        self.description = description

    # getter function for name
    @property
    def name(self):
        return self._name
    # setter function for name
    @name.setter
    def name(self, value):
        if type(value) is str:
            self._name = value.upper()
        else:
            raise ValueError("Name must be characters")

    # getter function for production numbers
    @property
    def in_pr(self):
        return self._in_pr
    # setter function for production numbers
    @in_pr.setter
    def in_pr(self, value):
        if type(value) is int:
            self._in_pr = value
        else:
            raise ValueError("Production models must be a number")

    # getter function for discontinued numbers
    @property
    def ds_pr(self):
        return self._ds_pr
    # setter function for discontinued numbers
    @ds_pr.setter
    def ds_pr(self, value):
        if type(value) is int:
            self._ds_pr = value
        else:
            raise ValueError("Discontinued models must be a number")

    # returns all the names of companies
    def all_companies():
        # grabs all names from the database
        cursor.execute(
            '''
            SELECT name FROM companies
            '''
        )
        # fetches them all
        companies_all = cursor.fetchall()
        # checks if the instance is itself, else returns a ValueError
        if companies_all:
            return [company[0] for company in companies_all]
        else:
            raise ValueError("Couldn't find companies ¯\_(ツ)_/¯")

    # returns an id of a company name inputted whether it is lowercase or uppercase
    def get_company_info(name):
        # uppercases the input
        name = name.upper()
        # fetches that data from the database
        cursor.execute(
            '''
            SELECT * FROM companies
            WHERE name = ?
            ''', (name,)
        )
        # fetches that single instance
        company_id = cursor.fetchone()
        # if it is that instance then returns the id, otherwise raises a ValueError
        if company_id:
            return company_id[0]
        else:
            raise ValueError("Could not find the id of company")

    # takes an input of an id and returns name, production numbers, and description
    def get_by_id(company_id):
        # fetches by id
        company = cursor.execute(
            '''
            SELECT * FROM companies
            WHERE id = ?
            ''',(company_id,)
        ).fetchone()
        # checks if it's an instance and returns all data, otherwise raises a ValuuError
        if company:
            return company[1], company[2], company[3], company[4]
        else:
            raise ValueError("Info does not exist")

    # takes the data of an initiated object and inserts into the database
    def save(self):
        # inserts into database and commits it
        new_company = cursor.execute(
            '''
            INSERT INTO companies(name, in_pr, ds_pr, description)
            VALUES(?, ?, ?, ?)
            ''',(self.name, self.in_pr, self.ds_pr, self.description)
        )
        conncection.commit()

    # takes in an update name and an id and updates the table
    def update(new_name, company_id):
        # updates the table and commits to the database
        cursor.execute(
            '''
            UPDATE companies
            SET name = ?
            WHERE id = ?
            ''',(new_name, company_id)
        )
        conncection.commit()

    # takes in an id and deletes that data from the table
    def delete(company_id):
        # deletes row from the tables and commits
        cursor.execute(
            '''
            DELETE FROM companies
            WHERE id = ?
            ''',(company_id,)
        )
        conncection.commit()
    
    # makes the prints of any instance look cleaner
    def __repr__(self):
        return f"{self.name}, {self.in_pr}, {self.ds_pr}"

# the class that holds and initalizes all models of a company
class Car:

    # initializes the class with model, type, generations, years, production, and company id
    def __init__(self, model, typeof, generations, years, in_pr, company_id):
        self.model = model
        self.typeof = typeof
        self.generations = generations
        self.years = years
        self.in_pr = in_pr
        self.company_id = company_id

    # getter function for the model
    @property
    def model(self):
        return self._model
    # setter function for the model
    @model.setter
    def model(self, value):
        if type(value) is str:
            self._model = value
        else:
            raise ValueError("Type in characters plz")

    # getter function for the type
    @property
    def typeof(self):
        return self._typeof
    # setter function for the type 
    @typeof.setter
    def typeof(self, value):
        if type(value) is str:
            self._typeof = value
        else:
            raise ValueError("Type in characters, no other data type")

    # getter function for the generations
    @property
    def generations(self):
        return self._generations
    # setter function for generations
    @generations.setter
    def generations(self, value):
        if type(value) is int:
            self._generations = value
        else:
            raise ValueError("Type in a number, not that you dum dum")

    # getter function for the years
    @property
    def years(self):
        return self._years
    # setter function for the years
    @years.setter
    def years(self, value):
        if type(value) is str:
            self._years = value
        else:
            raise ValueError("Please type in valid year info")

    # getter function for the production
    @property
    def in_pr(self):
        return self._in_pr
    # setter function for the production
    @in_pr.setter
    def in_pr(self, value):
        if type(value) is bool:
            self._in_pr = value
        else:
            raise ValueError("Needs to be True or false statement")

    # getter function for the company id
    @property
    def company_id(self):
        return self._company_id
    # setter function for the company id
    @company_id.setter
    def company_id(self, value):
        if type(value) is int:
            self._company_id = value
        else:
            raise ValueError("Must be a number, try again bozo")

    # takes in the model name and returns the id of the model
    @classmethod
    def get_model_id(cls, name):
        # grabs the object from the table
        cursor.execute(
            '''
            SELECT * FROM cars
            WHERE model = ?
            ''', (name,)
        )
        # fetches the single
        car_id = cursor.fetchone()
        # if the instance is itself, it returns an id, otherwise it raises a ValueError
        if car_id:
            return car_id[0]
        else:
            raise ValueError("Could not find the id of model")

    # takes the input of the id and fetches car information
    @classmethod
    def get_by_id(cls, model_id):
        # grabs the model by the id
        model = cursor.execute(
            '''
            SELECT * FROM cars
            WHERE id = ?
            ''',(model_id,)
        ).fetchone()
        # if the instance is itself, it returns all the car info
        if model:
            return model[1], model[2], model[3], model[4], model[5]
        else:
            raise ValueError("Info does not exist")

    # takes an input of the id of the company and returns all car models with the same id
    @classmethod
    def get_company_models(cls, company_id):
        # fetches all models
        models = cursor.execute(
            '''
            SELECT model FROM cars
            WHERE company_id = ?
            ''',(company_id,)
        ).fetchall()
        # if the instance is itself, returns all the names otherwise it raises a ValueError
        if models:
            return [model[0] for model in models]
        else:
            raise ValueError("Could not find models of company")

    # inserts into the database a new car instance
    def save(model, typeof, generations, years, in_pr, company_id):
        # inserts data into the database and commits it
        new_company = cursor.execute(
            '''
            INSERT INTO cars(model, type, generations, years, in_pr, company_id)
            VALUES(?, ?, ?, ?, ?, ?)
            ''',(model, typeof, generations, years, in_pr, company_id)
        )
        conncection.commit()

    # takes in a new name and model id and updates the car
    def update(new_name, model_id):
        # puts in the id and new name and commits it to the database
        cursor.execute(
            '''
            UPDATE cars
            SET model = ?
            WHERE id = ?
            ''',(new_name, model_id)
        )
        conncection.commit()

    # takes in the id and deletes that car
    def delete(model_id):
        # takes the id and deletes the car and commits it to the database
        cursor.execute(
            '''
            DELETE FROM cars
            WHERE id = ?
            ''',(model_id,)
        )
        conncection.commit()

    # Makes the Car instance look cleaner
    def __repr__(self):
        return f"{self.model}, {self.typeof}, {self.generations}, {self.years}, {self.in_pr}"
