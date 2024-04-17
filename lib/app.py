import sqlite3
import inquirer
from pprint import pprint
import os
conncection = sqlite3.connect("cars.db")
cursor = conncection.cursor()

title_art = """
_________                  ______________                     _____      ______     
__  ____/_____ ________    __  ____/__  /________________________(_)________  /____ 
_  /    _  __ `/_  ___/    _  /    __  __ \_  ___/  __ \_  __ \_  /_  ___/_  /_  _ \\
/ /___  / /_/ /_  /        / /___  _  / / /  /   / /_/ /  / / /  / / /__ _  / /  __/
\____/  \__,_/ /_/         \____/  /_/ /_//_/    \____//_/ /_//_/  \___/ /_/  \___/
"""

class Company:

    def __init__(self, name, in_pr, ds_pr):
        self.name = name
        self.in_pr = in_pr
        self.ds_pr = ds_pr

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        if type(value) is str:
            self._name = value.upper()
        else:
            raise ValueError("Name must be characters")

    @property
    def in_pr(self):
        return self._in_pr
    @in_pr.setter
    def in_pr(self, value):
        if type(value) is int:
            self._in_pr = value
        else:
            raise ValueError("Production models must be a number")

    @property
    def ds_pr(self):
        return self._ds_pr
    @ds_pr.setter
    def ds_pr(self, value):
        if type(value) is int:
            self._ds_pr = value
        else:
            raise ValueError("Discontinued models must be a number")

    def all_companies():
        cursor.execute(
            '''
            SELECT name FROM companies
            '''
        )
        companies_all = cursor.fetchall()
        if companies_all:
            return [company[0] for company in companies_all]
        else:
            raise ValueError("Couldn't find companies ¯\_(ツ)_/¯")

    def get_company_info(name):
        name = name.upper()
        cursor.execute(
            '''
            SELECT * FROM companies
            WHERE name = ?
            ''', (name,)
        )
        company_id = cursor.fetchone()
        if company_id:
            return company_id[0]
        else:
            raise ValueError("Could not find the id of company")

    def get_by_id(company_id):
        company = cursor.execute(
            '''
            SELECT * FROM companies
            WHERE id = ?
            ''',(company_id,)
        ).fetchone()
        if company:
            return company[1], company[2], company[3], company[4]
        else:
            raise ValueError("Info does not exist")

    def save(self):
        new_company = cursor.execute(
            '''
            INSERT INTO companies(name, in_pr, ds_pr)
            VALUES(?, ?, ?)
            ''',(self.name, self.in_pr, self.ds_pr)
        )
        conncection.commit()

    def update(new_name, company_id):
        cursor.execute(
            '''
            UPDATE companies
            SET name = ?
            WHERE id = ?
            ''',(new_name, company_id)
        )
        conncection.commit()

    def delete(company_id):
        cursor.execute(
            '''
            DELETE FROM companies
            WHERE id = ?
            ''',(company_id,)
        )
        conncection.commit()
    
    def __repr__(self):
        return f"{self.name}, {self.in_pr}, {self.ds_pr}"

class Car:

    def __init__(self, model, typeof, generations, years, in_pr, company_id):
        self.model = model
        self.typeof = typeof
        self.generations = generations
        self.years = years
        self.in_pr = in_pr
        self.company_id = company_id

    @property
    def model(self):
        return self._model
    @model.setter
    def model(self, value):
        if type(value) is str:
            self._model = value
        else:
            raise ValueError("Type in characters plz")

    @property
    def typeof(self):
        return self._typeof
    @typeof.setter
    def typeof(self, value):
        if type(value) is str:
            self._typeof = value
        else:
            raise ValueError("Type in characters, no other data type")

    @property
    def generations(self):
        return self._generations
    @generations.setter
    def generations(self, value):
        if type(value) is int:
            self._generations = value
        else:
            raise ValueError("Type in a number, not that you dum dum")

    @property
    def years(self):
        return self._years
    @years.setter
    def years(self, value):
        if type(value) is str:
            self._years = value
        else:
            raise ValueError("Please type in valid year info")

    @property
    def in_pr(self):
        return self._in_pr
    @in_pr.setter
    def in_pr(self, value):
        if type(value) is bool:
            self._in_pr = value
        else:
            raise ValueError("Needs to be True or false statement")

    @property
    def company_id(self):
        return self._company_id
    @company_id.setter
    def company_id(self, value):
        if type(value) is int:
            self._company_id = value
        else:
            raise ValueError("Must be a number, try again bozo")

    @classmethod
    def get_model_id(cls, name):
        cursor.execute(
            '''
            SELECT * FROM cars
            WHERE model = ?
            ''', (name,)
        )
        car_id = cursor.fetchone()
        if car_id:
            return car_id[0]
        else:
            raise ValueError("Could not find the id of model")

    @classmethod
    def get_by_id(cls, model_id):
        model = cursor.execute(
            '''
            SELECT * FROM cars
            WHERE id = ?
            ''',(model_id,)
        ).fetchone()
        if model:
            return model[1], model[2], model[3], model[4], model[5]
        else:
            raise ValueError("Info does not exist")

    @classmethod
    def get_company_models(cls, company_id):
        models = cursor.execute(
            '''
            SELECT model FROM cars
            WHERE company_id = ?
            ''',(company_id,)
        ).fetchall()
        if models:
            return [model[0] for model in models]
        else:
            raise ValueError("Could not find models of company")

    def save(model, typeof, generations, years, in_pr, company_id):
        new_company = cursor.execute(
            '''
            INSERT INTO cars(model, type, generations, years, in_pr, company_id)
            VALUES(?, ?, ?, ?, ?, ?)
            ''',(model, typeof, generations, years, in_pr, company_id)
        )
        conncection.commit()

    def update(new_name, company_id):
        cursor.execute(
            '''
            UPDATE cars
            SET model = ?
            WHERE id = ?
            ''',(new_name, company_id)
        )
        conncection.commit()

    def delete(company_id):
        cursor.execute(
            '''
            DELETE FROM cars
            WHERE id = ?
            ''',(company_id,)
        )
        conncection.commit()

fake_model = Car("Cadillac Fleetwood", "sedan", 5, "1948-present", True, 17)

if __name__ == "__main__":
    print(f"{title_art}\n")
    print("Welcome to Car Chronicle!\n")

    while True:
        options = [
            inquirer.List(
                "choice",
                message = "Select your next operation",
                choices = ["Choose Car Company", "Search Car Company", "Create Company", "Update Company", "Delete Company", "Search Car", "Create Car", "Exit"],
            ),
        ]
        answers = inquirer.prompt(options)
        if answers['choice'] == "Choose Car Company":
            car_list = [
                inquirer.List(
                    "car_choice",
                    message = "Choose a Car company",
                    choices = Company.all_companies()
                ),
            ]
            car_answers = inquirer.prompt(car_list)
            chosen_company = car_answers["car_choice"]
            chosen_company_id = Company.get_company_info(chosen_company)
            manufacture_info = Company.get_by_id(chosen_company_id)
            models = Car.get_company_models(chosen_company_id)
            print(manufacture_info[0])
            print()
            print("Models/Trims currently produced:", manufacture_info[1])
            print("Discontinued Models:", manufacture_info[2])
            print()
            print("Description:\n")
            if manufacture_info[3] == "Null":
                print("There is no description in the database")
            else:
                print(manufacture_info[3])
            print()
            print("Models:")
            model_list = [
                inquirer.List(
                    "model_choice",
                    message = "Choose a Model",
                    choices = models
                )
            ]
            model_answers = inquirer.prompt(model_list)
            model_id = Car.get_model_id(model_answers['model_choice'])
            car_info = Car.get_by_id(model_id)
            print(car_info[0])
            print(car_info[1])
            if car_info[4] == True:
                print("This vehicle is currently in production,", car_info[3])
                if int(car_info[2]) == 1:
                    print("Right now there is only 1 generation of this vehicle")
                else:
                    print("Right now there is", car_info[2], "generations of this vehicle")
            else:
                print("This was produced in between", car_info[3])
                if int(car_info[2]) == 1:
                    print("There was only 1 generation of this vehicle")
                else:
                    print("There was", car_info[2], "generations of this vehicle")
            options_list = [
                inquirer.List(
                    "option_choice",
                    message = "What would you like to do with this car model?",
                    choices = ["Continue Browsing", "Delete Car", "Update Car"],
                ),
            ]
            answers = inquirer.prompt(options_list)
            if answers['option_choice'] == "Continue Browsing":
                os.system('clear')
            elif answers['option_choice'] == "Delete Car":
                os.system('clear')
                Car.delete(model_id)
                print("Car deleted\n")
            elif answers['option_choice'] == "Update Car":
                new_name = input("Type in what you would like to rename the model to:").capitalize()
                Car.update(new_name, model_id)

        elif answers['choice'] == "Search Car Company":
            typed = input("Type in car company name: ")
            chosen_company_id = Company.get_company_info(typed)
            manufacture_info = Company.get_by_id(chosen_company_id)
            models = Car.get_company_models(chosen_company_id)
            print()
            print(manufacture_info[0])
            print()
            print("Models/Trims currently produced:", manufacture_info[1])
            print("Discontinued Models:", manufacture_info[2])
            print()
            print("Description:\n")
            if manufacture_info[3] == "Null":
                print("There is no description in the database\n")
            else:
                print(manufacture_info[3])
                print()
            print("Models:")
            model_list = [
                inquirer.List(
                    "model_choice",
                    message = "Choose a Model",
                    choices = models
                )
            ]
            model_answers = inquirer.prompt(model_list)
            model_id = Car.get_model_id(model_answers['model_choice'])
            car_info = Car.get_by_id(model_id)
            print(car_info[0])
            print(car_info[1])
            if car_info[4] == True:
                print("This vehicle is currently in production,", car_info[3])
                if int(car_info[2]) == 1:
                    print("Right now there is only 1 generation of this vehicle")
                else:
                    print("Right now there is", car_info[2], "generations of this vehicle")
            else:
                print("This was produced in between", car_info[3])
                if int(car_info[2]) == 1:
                    print("There was only 1 generation of this vehicle")
                else:
                    print("There was", car_info[2], "generations of this vehicle")
            options_list = [
                inquirer.List(
                    "option_choice",
                    message = "What would you like to do with this car model?",
                    choices = ["Continue Browsing", "Delete Car", "Update Car"],
                ),
            ]
            answers = inquirer.prompt(options_list)
            if answers['option_choice'] == "Continue Browsing":
                os.system('clear')
            elif answers['option_choice'] == "Delete Car":
                os.system('clear')
                Car.delete(model_id)
                print("Car deleted\n")
            elif answers['option_choice'] == "Update Car":
                new_name = input("Type in what you would like to rename the model to:").capitalize()
                Car.update(new_name, model_id)

        elif answers['choice'] == "Create Company":
            new_name = input("Type in Company Name: ")
            new_production = input("Type how many models are being currently produced: ")
            new_discontinued = input("Type how many models have been discontinued: ")
            new_company = Company(new_name, int(new_production), int(new_discontinued))
            new_company.save()

        elif answers['choice'] == "Update Company":
            choose_company = input("Type in company you want to update: ")
            update_name = input("Type in what you want to change the company name to: ").upper()
            chosen_company_id = Company.get_company_info(choose_company)
            Company.update(update_name, chosen_company_id)

        elif answers['choice'] == "Delete Company":
            choose_company = input("Type in which company you would like to delete: ")
            chosen_company_id = Company.get_company_info(choose_company)
            Company.delete(chosen_company_id)

        elif answers['choice'] == "Search Car":
            print("Note: Unless what you type in the exact same as the database, it will not return anything")
            lotum = input("Type in the model you would Like to see: ")
            chosen_model = Car.get_model_id(lotum)
            model_info = Car.get_by_id(chosen_model)
            print()
            print(model_info[0])
            print(model_info[1])
            if model_info[4] == True:
                print("This vehicle is currently in production,", model_info[3])
                if int(model_info[2]) == 1:
                    print("Right now there is only 1 generation of this vehicle\n")
                else:
                    print("Right now there is", model_info[2], "generations of this vehicle\n")
            else:
                print("This was produced in between", model_info[3])
                if int(model_info[2]) == 1:
                    print("There was only 1 generation of this vehicle\n")
                else:
                    print("There was", model_info[2], "generations of this vehicle\n")

        elif answers['choice'] == "Create Car":
            company_model_id = input("Type in the company that this new model is made by: ")
            company_name = company_model_id.upper()
            chosen_company_id = Company.get_company_info(company_model_id)
            car_model = input("Type in what the name of this model is: ").capitalize()
            full_car_model_name = f"{company_name} {car_model}"
            car_type = input("Type in what type of car this is(example: coupe): ").capitalize()
            car_generations = input("Type in how many generations this car has had: ")
            car_years = input("Type in what years this car was produced: ")
            bool_list = [
                inquirer.List(
                    "choice",
                    message = "Is this Car still in production?",
                    choices = ["Yes", "No"],
                ),
            ]
            model_answers = inquirer.prompt(bool_list)
            if model_answers['choice'] == "Yes":
                car_bool = True
            else:
                car_bool = False
            Car.save(full_car_model_name, car_type, int(car_generations), car_years, car_bool, chosen_company_id)
            print("Car added successfully\n")

        elif answers['choice'] == "Exit":
            break
