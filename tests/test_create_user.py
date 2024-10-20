import allure
import requests

from src.data import Data
from src.endpoints import CREATE_USER
from src.helper import generate_random_string


class TestCreateUser:

    @allure.title('Создание нового пользователя')
    def test_create_new_user(self):
        name = generate_random_string()
        email = generate_random_string()+Data.EMAIL
        password = generate_random_string()

        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(Data.URL+CREATE_USER, data=payload)
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert response.json()['user']['name'] == name

    @allure.title('Создание уже существующего пользователя')
    def test_create_user_that_already_exists(self, create_user):
        payload = {
            "email": create_user[0],
            "password": create_user[1],
            "name": create_user[2]
        }
        response = requests.post(Data.URL+CREATE_USER, data=payload)
        assert response.status_code == 403
        assert response.json()['success'] is False
        assert response.json()['message'] == Data.USER_EXISTS

    @allure.title('Создание нового пользователя без одного поля данных')
    def test_create_user_without_one_field(self, create_user):
        payload = {
            "email": create_user[0],
            "password": create_user[1]
        }
        response = requests.post(Data.URL + CREATE_USER, data=payload)
        assert response.status_code == 403
