# Car Chronicle

Car Chronicle is a Python application that allows users to interact with a database of car companies and their models. 

Users can perform various operations such as viewing company information, searching for specific car models, 
creating new companies and cars, updating existing entries, and deleting entries. 

The reason why I wanted to create this app was that I have always loved cars since I was a little kid, 
and there are thousands of models that exist that I have no knowledge of and dozens of companies that I do not know exist. 

So I created this so I can browse an archive of majority of car companies and models that have existed. 
Stretching all the way back from 1899 to present day, the amount of models in the database reaching close to 3000.

## Features

- **Browse Car Companies**: View a list of car companies and view its details.
- **Search Car Companies**: Search for a specific car company by name and view its details.
- **View Car Models**: Browse through car models produced by a selected company, view details such as generations, production status, and years.
- **Create Company**: Add a new car company to the database with information about its production and discontinued models.
- **Update Company**: Modify the details of an existing car company, including its name and production/discontinued model counts.
- **Delete Company**: Permanently remove a car company from the database.
- **Search Car**: Search for a specific car model by name and view its details.
- **Create Car**: Add a new car model to the database, specifying its company, name, type, generations, years, and production status.
- **Update Car**: Modify the details of an existing car model, including its name and production status.
- **Delete Car**: Permanently remove a car model from the database.

## Installation

once you have cloned the repository to your machine type into the terminal `pipenv install`

## Usage

- initiate the shell with `pipenv shell`
- run `seed.py` within the /lib to populate the database (this file will take approximately 1 minute to finish)
- run `app.py` within the /lib to start the application
- use the app the way you like, selecting exit once you are finished
- enjoy!

## Credits

Thank you [AutoEvolution](https://www.autoevolution.com/cars/) for the (mostly) well built database of cars