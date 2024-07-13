from models import *
import sqlite3
import inquirer
import os
conncection = sqlite3.connect("cars.db")
cursor = conncection.cursor()

# variable that holds the title at the top of the program
title_art = """
_________                  ______________                     _____      ______     
__  ____/_____ ________    __  ____/__  /________________________(_)________  /____ 
_  /    _  __ `/_  ___/    _  /    __  __ \_  ___/  __ \_  __ \_  /_  ___/_  /_  _ \\
/ /___  / /_/ /_  /        / /___  _  / / /  /   / /_/ /  / / /  / / /__ _  / /  __/
\____/  \__,_/ /_/         \____/  /_/ /_//_/    \____//_/ /_//_/  \___/ /_/  \___/
"""

# the main application that the user interacts with
if __name__ == "__main__":

    # the while loop that runs during the entirety of the application
    while True:
        # intro text
        print(f"{title_art}\n")
        print("Welcome to Car Chronicle!\n")
        # initial list of options for the user to select from
        options = [
            inquirer.List(
                "choice",
                message = "Select your next operation",
                choices = ["Choose Car Company", "Search Car Company", "Create Company", "Update Company", "Delete Company", "Search Car", "Create Car", "Exit"],
            ),
        ]
        # the response of that list
        answers = inquirer.prompt(options)
        # the first option choice, creating another list of all the car companies
        if answers['choice'] == "Choose Car Company":
            car_list = [
                inquirer.List(
                    "car_choice",
                    message = "Choose a Car company",
                    choices = Company.all_companies()
                ),
            ]
            os.system('clear')
            # choice of car company
            car_answers = inquirer.prompt(car_list)
            chosen_company = car_answers["car_choice"]
            # the id of the chosen car company
            chosen_company_id = Company.get_company_info(chosen_company)
            # the information of the car company
            manufacture_info = Company.get_by_id(chosen_company_id)
            # all the models of that car company
            models = Car.get_company_models(chosen_company_id)
            # prints all the manufacture information
            os.system('clear')
            print(manufacture_info[0])
            print("\nModels/Trims currently produced:", manufacture_info[1])
            print("Discontinued Models:", manufacture_info[2])
            # checks if the description is empty, prints a message if it is and prints the description if it isn't
            if manufacture_info[3] == "":
                print("\nThere is no description in the database")
            else:
                print("\nDescription:\n")
                print(manufacture_info[3])
            print("\nModels:")
            # creates a list of models by that company
            model_list = [
                inquirer.List(
                    "model_choice",
                    message = "Choose a Model",
                    choices = models
                )
            ]
            # the response of that list
            model_answers = inquirer.prompt(model_list)
            # gets the id of that model chosen
            model_id = Car.get_model_id(model_answers['model_choice'])
            # gets all the information with the retrieved id
            car_info = Car.get_by_id(model_id)
            # prints model info
            os.system('clear')
            print(car_info[0])
            print(car_info[1])
            # prints different text based on whether the car is currently in production
            if car_info[4] == True:
                print("This vehicle is currently in production,", car_info[3])
                if int(car_info[2]) == 1:
                    print("Right now there is only 1 generation of this vehicle\n")
                else:
                    print("Right now there is", car_info[2], "generations of this vehicle\n")
            else:
                print("This was produced in between", car_info[3])
                if int(car_info[2]) == 1:
                    print("There was only 1 generation of this vehicle\n")
                else:
                    print("There was", car_info[2], "generations of this vehicle\n")
            # gives a user options to delete the car, update it or keep browsing
            options_list = [
                inquirer.List(
                    "option_choice",
                    message = "What would you like to do with this car model?",
                    choices = ["Continue Browsing", "Delete Car", "Update Car"],
                ),
            ]
            # keeps the response of the user
            answers = inquirer.prompt(options_list)
            # clears the terminal and returns back to the menu
            if answers['option_choice'] == "Continue Browsing":
                os.system('clear')
            # allows the user to delete the car and returns back to the menu
            elif answers['option_choice'] == "Delete Car":
                os.system('clear')
                Car.delete(model_id)
                print("Car deleted\n")
            # lets the user type in what they would like to change the name to
            elif answers['option_choice'] == "Update Car":
                new_name = input("Type in what you would like to rename the model to: ").capitalize()
                Car.update(new_name, model_id)
                os.system('clear')
                print("Car updated\n")

        # allows user to type in car company name and browse from there
        elif answers['choice'] == "Search Car Company":
            # user types in the company name
            typed = input("Type in car company name: ")
            # gets the id from the input
            chosen_company_id = Company.get_company_info(typed)
            # grabs the information from that id
            manufacture_info = Company.get_by_id(chosen_company_id)
            # grabs all the models associated with that company id
            models = Car.get_company_models(chosen_company_id)
            os.system('clear')
            # prints all the information
            print(manufacture_info[0])
            print("\nModels/Trims currently produced:", manufacture_info[1])
            print("Discontinued Models:", manufacture_info[2])
            # checks if the description is empty, prints a message if it is and prints the description if it isn't
            if manufacture_info[3] == "":
                print("\nThere is no description in the database")
            else:
                print("\nDescription:\n")
                print(manufacture_info[3])
            print("\nModels:")
            # creates a list of models by that company
            model_list = [
                inquirer.List(
                    "model_choice",
                    message = "Choose a Model",
                    choices = models
                )
            ]
            # the response of that list
            model_answers = inquirer.prompt(model_list)
            # gets the id of that model chosen
            model_id = Car.get_model_id(model_answers['model_choice'])
            # gets all the information with the retrieved id
            car_info = Car.get_by_id(model_id)
            # prints model info
            os.system('clear')
            print(car_info[0])
            print(car_info[1])
            # prints different text based on whether the car is currently in production
            if car_info[4] == True:
                print("This vehicle is currently in production,", car_info[3])
                if int(car_info[2]) == 1:
                    print("Right now there is only 1 generation of this vehicle\n")
                else:
                    print("Right now there is", car_info[2], "generations of this vehicle\n")
            else:
                print("This was produced in between", car_info[3])
                if int(car_info[2]) == 1:
                    print("There was only 1 generation of this vehicle\n")
                else:
                    print("There was", car_info[2], "generations of this vehicle\n")
            # gives a user options to delete the car, update it or keep browsing
            options_list = [
                inquirer.List(
                    "option_choice",
                    message = "What would you like to do with this car model?",
                    choices = ["Continue Browsing", "Delete Car", "Update Car"],
                ),
            ]
            # keeps the response of the user
            answers = inquirer.prompt(options_list)
            # clears the terminal and returns back to the menu
            if answers['option_choice'] == "Continue Browsing":
                os.system('clear')
            # allows the user to delete the car and returns back to the menu
            elif answers['option_choice'] == "Delete Car":
                os.system('clear')
                Car.delete(model_id)
                print("Car deleted\n")
            # lets the user type in what they would like to change the name to
            elif answers['option_choice'] == "Update Car":
                new_name = input("Type in what you would like to rename the model to: ").capitalize()
                Car.update(new_name, model_id)
                os.system('clear')
                print("Car updated\n")

        # allows user to type in company name, production numbers, and description and create a new company
        elif answers['choice'] == "Create Company":
            # takes the input of the user and uppercases it
            new_name = input("Type in Company Name: ").upper()
            # takes in how many models are currently being produced
            new_production = int(input("Type how many models are being currently produced: "))
            # takes in how many models have been discontinued
            new_discontinued = int(input("Type how many models have been discontinued: "))
            # takes in the description of the car company
            new_description = input("Type a description of this car company: ")
            # creates an instance of that car company and turns production numbers into an integer
            new_company = Company(new_name, new_production, new_discontinued, new_description)
            # saves that info and inserts into the table
            new_company.save()
            os.system('clear')
            print("Company Created successfully\n")

        # allows users to type in a car company and change it's name
        elif answers['choice'] == "Update Company":
            # takes in the typed info of the company the user wants to update
            choose_company = input("Type in company you want to update: ")
            # takes in the new company name and updates it
            update_name = input("Type in what you want to change the company name to: ").upper()
            # gets the id of the company that was initially typed in
            chosen_company_id = Company.get_company_info(choose_company)
            # updates the table with the new information
            Company.update(update_name, chosen_company_id)
            os.system('clear')
            print("Company Updated successfully\n")

        # allows user to type in a company and deletes that company
        elif answers['choice'] == "Delete Company":
            # takes in the input of the company that the user wants to delete
            choose_company = input("Type in which company you would like to delete: ")
            # takes in that input and grabs the id of the desired company
            chosen_company_id = Company.get_company_info(choose_company)
            # takes that id and deletes the company from the table
            Company.delete(chosen_company_id)
            os.system('clear')
            print("Company Deleted successfully\n")

        # allows user to search by car model name, although very inconsistent due to web scraping data
        elif answers['choice'] == "Search Car":
            print("Note: Unless you type in the exact same model as the database, it will not return anything")
            # takes the input of the model name
            lotum = input("Type in the model you would Like to see: ")
            # gets the id of that input
            chosen_model = Car.get_model_id(lotum)
            # grabs that data for that model
            model_info = Car.get_by_id(chosen_model)
            os.system('clear')
            # prints the model info
            print()
            print(model_info[0])
            print(model_info[1])
            # prints different messages depending if the car is currently in production or not
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
            # gives a user options to delete the car, update it or keep browsing
            options_list = [
                inquirer.List(
                    "option_choice",
                    message = "What would you like to do with this car model?",
                    choices = ["Continue Browsing", "Delete Car", "Update Car"],
                ),
            ]
            # keeps the response of the user
            answers = inquirer.prompt(options_list)
            # clears the terminal and returns back to the menu
            if answers['option_choice'] == "Continue Browsing":
                os.system('clear')
            # allows the user to delete the car and returns back to the menu
            elif answers['option_choice'] == "Delete Car":
                os.system('clear')
                Car.delete(chosen_model)
                print("Car deleted\n")
            # lets the user type in what they would like to change the name to
            elif answers['option_choice'] == "Update Car":
                new_name = input("Type in what you would like to rename the model to: ").capitalize()
                Car.update(new_name, chosen_model)
                os.system('clear')
                print("Car updated\n")
            

        # allows user to create a new car model, typing in name, years, type, generations, if it's still in production and the company id
        elif answers['choice'] == "Create Car":
            # takes in the name of the company
            company_model_id = input("Type in the company that this new model is made by: ")
            # takes that input and uppercases it for the model name that is put into the table
            company_name = company_model_id.upper()
            # gets the id of the company that was chosen
            chosen_company_id = Company.get_company_info(company_model_id)
            # takes an input of the new car model name
            car_model = input("Type in what the name of this model is: ").capitalize()
            # takes the uppercased company name and the new car model name and makes it one variable
            full_car_model_name = f"{company_name} {car_model}"
            # takes the type of the new car model
            car_type = input("Type in what type of car this is(example: coupe): ").capitalize()
            # takes in how many car generations this new car has had
            car_generations = int(input("Type in how many generations this car has had: "))
            # takes in what years the new car was produced
            car_years = input("Type in what years this car was produced: ")
            # creates a list that lets the user dictate whether this car is still in production
            bool_list = [
                inquirer.List(
                    "choice",
                    message = "Is this Car still in production?",
                    choices = ["Yes", "No"],
                ),
            ]
            # the answer of that list
            model_answers = inquirer.prompt(bool_list)
            # sets the boolean of the production if it is yes, otherwise it is set to no
            if model_answers['choice'] == "Yes":
                car_bool = True
            else:
                car_bool = False
            # saves the new car model into the database and turns car generations into an integer
            Car.save(full_car_model_name, car_type, car_generations, car_years, car_bool, chosen_company_id)
            os.system('clear')
            print("Car added successfully\n")

        # clears the terminal and quits the app
        elif answers['choice'] == "Exit":
            os.system('clear')
            break
