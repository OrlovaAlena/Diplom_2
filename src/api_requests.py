import pytest
import requests

from src.data import Data
from src.endpoints import CREATE_USER, USER, INGREDIENTS
from src.helper import generate_random_string


def create_new_user():
    name = generate_random_string()
    email = generate_random_string() + Data.EMAIL
    password = generate_random_string()

    login_pass = []

    payload = {
        "email": email,
        "password": password,
        "name": name
    }
    response = requests.post(Data.URL + CREATE_USER, data=payload)
    if response.status_code == 200:
        login_pass.append(email)
        login_pass.append(password)
        login_pass.append(name)
        token = response.json()['accessToken']
        login_pass.append(token)

    return login_pass


def delete_user(token):
    return requests.delete(Data.URL+USER, headers={'Authorization': f'{token}'})


# def get_ingredients():
#     ingredients = requests.get(Data.URL + INGREDIENTS)
#     return ingredients.json()['data']
#
#

