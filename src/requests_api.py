import requests

from src.data import Data
from src.endpoints import CREATE_USER, USER
from src.helper import generate_random_string


def create_new_user():
    name = generate_random_string(8)
    email = generate_random_string(7) + Data.EMAIL
    password = generate_random_string(6)

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
