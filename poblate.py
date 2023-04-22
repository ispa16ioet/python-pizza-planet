import requests
from faker import Faker

import json
import random
import datetime

fake = Faker()
ingredients = [
    {"name": "Mozzarella cheese", "price": 2.50},
    {"name": "Pepperoni", "price": 1.75},
    {"name": "Ham", "price": 2.00},
    {"name": "Mushrooms", "price": 1.25},
    {"name": "Onion", "price": 0.75},
    {"name": "Bell pepper", "price": 1.00},
    {"name": "Olives", "price": 1.50},
    {"name": "Anchovies", "price": 2.25},
    {"name": "Italian sausage", "price": 2.50},
    {"name": "Bacon", "price": 2.00}
]
beverages = [
    {"name": "Coca-Cola", "price": 1.50},
    {"name": "Pepsi", "price": 1.50},
    {"name": "Sprite", "price": 1.25},
    {"name": "Fanta Orange", "price": 1.25},
    {"name": "Lemonade", "price": 1.75},
    {"name": "Iced tea", "price": 1.75},
    {"name": "Coffee", "price": 1.50},
    {"name": "Hot chocolate", "price": 2.00},
    {"name": "Orange juice", "price": 2.25},
    {"name": "Milk", "price": 1.00}
]
sizes = [
    {"name": "Personal", "price": 6.99},
    {"name": "Small", "price": 9.99},
    {"name": "Medium", "price": 12.99},
    {"name": "Large", "price": 15.99},
    {"name": "Extra Large", "price": 18.99}
]

def generate_random_date():
    month = random.randint(1, 12)
    day = random.randint(1, 28)  
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    microsecond = random.randint(0, 999999)

    # Get the current year
    current_year = datetime.date.today().year

    # Construct the datetime object with the current year, random month, day, hour, minute, second, and microsecond
    random_datetime = datetime.datetime(current_year, month, day, hour, minute, second, microsecond)

    # Format the datetime as needed
    random_datetime_string = random_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')
    return(random_datetime_string)

def postData(url, data):
    link = f'http://127.0.0.1:5000/{url}/'
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(link, data=json_data, headers=headers)
    return response

def create_models(model, data):
    for dict in data:
        postData(model, dict)

def generate_random_list_of_ids(limit):
    length = random.randint(1, limit)
    random_list = [fake.random_int(min=1, max=limit) for _ in range(length)]
    return random_list


def generate_random_list_of_names():
    names = [fake.name() for _ in range(350)]
    return names

def create_ramdon_order(fake_names):
    name = fake_names[fake.random_int(min=0, max=349)]
    dni = fake.random_int(min=10000000, max=99999999)
    phone_number = fake.phone_number()
    address = fake.address()
    size_id = fake.random_int(min=1, max=5)
    date = generate_random_date()

    # Generate a random list of ingredients, beverages
    ingredients = generate_random_list_of_ids(10)
    beverages = generate_random_list_of_ids(10)
    

    data = {
        'client_name': name, 
        'client_dni': dni, 
        'state': 'finish', 
        'client_address': address, 
        'client_phone': phone_number, 
        'size_id': size_id, 
        'ingredients': ingredients, 
        'beverages': beverages,
        'date':date
    }
    return data

models = [
    {'name': 'ingredient', 'data': ingredients},
    {'name': 'beverage', 'data': beverages},
    {'name': 'size', 'data': sizes}
]

for model in models:
    create_models(model['name'],model['data'])
fake_names = generate_random_list_of_names()
for i in range(1,1000):
    create_models('order',[create_ramdon_order(fake_names)])