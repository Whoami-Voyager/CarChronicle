import sqlite3
import inquirer
from pprint import pprint
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

    @classmethod
    def all_companies(cls):
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

    def get_by_id(company_id):
        company = cursor.execute(
            '''
            SELECT * FROM companies
            WHERE id = ?
            ''',(company_id,)
        ).fetchone()
        if company:
            return company[1], company[2], company[3]
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


fake_company = Company("Packard", 4, 5)

if __name__ == "__main__":

    while True:
        print(f"{title_art}\n")
        print("Welcome to Car Chronicle!\n")
        options = [
            inquirer.List(
                "choice",
                message="Select your next operation",
                choices=["Choose Car Company", "Search Car Company", "Create Company", "Update Company", "Delete Company", "See Car Model info", "Create Car", "Update Car", "Delete Car", "Exit"],
            ),
        ]
        answers = inquirer.prompt(options)
        if answers['choice'] == "Choose Car Company":
            car_list = [
                inquirer.List(
                    "car_choice",
                    message="Choose a Car company",
                    choices=Company.all_companies()
                ),
            ]
            car_answers = inquirer.prompt(car_list)
            chosen_company = car_answers["car_choice"]
            chosen_company_id = Company.get_company_info(chosen_company)
            manufacture_info = Company.get_by_id(chosen_company_id)
            print(manufacture_info[0])
            print("Models/Trims currently produced:", manufacture_info[1])
            print("Discontinued Models:", manufacture_info[2])
            print("Models:")
        elif answers['choice'] == "Search Car Company":
            typed = input("Type in car company name: ")
            chosen_company_id = Company.get_company_info(typed)
            manufacture_info = Company.get_by_id(chosen_company_id)
            print()
            print(manufacture_info[0])
            print("Models/Trims currently produced:", manufacture_info[1])
            print("Discontinued Models:", manufacture_info[2])
            print("Models:")
        elif answers['choice'] == "Create Company":
            new_name = input("Type in Company Name: ")
            new_production = input("Type how many models are being currently produced: ")
            new_discontinued = input("Type how many models have been discontinued: ")
            new_company = Company(new_name, int(new_production), int(new_discontinued))
            new_company.save()
            conncection.commit()
        elif answers['choice'] == "Update Company":
            choose_company = input("Type in company you want to update: ")
            update_name = input("Type in what you want to change the company name to: ").upper()
            chosen_company_id = Company.get_company_info(choose_company)
            Company.update(update_name, chosen_company_id)
            conncection.commit()
        elif answers['choice'] == "Delete Company":
            choose_company = input("Type in which company you would like to delete: ")
            chosen_company_id = Company.get_company_info(choose_company)
            Company.delete(chosen_company_id)
            conncection.commit()
        elif answers['choice'] == "Exit":
            break
