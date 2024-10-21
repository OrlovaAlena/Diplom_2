import allure
import requests

from src.requests_api import delete_user
from src.data import Data
from src.endpoints import LOGIN


class TestLogin:

    @allure.title('Логин существующего пользователя')
    def test_login_new_user(self, create_user):
        payload = {
            "email": create_user[0],
            "password": create_user[1],
            "name": create_user[2]
        }
        token = create_user[3]
        response = requests.post(Data.URL+LOGIN, data=payload)

        assert response.status_code == 200
        assert response.json()['success'] is True

        delete_user(token)

    @allure.title('Логин несуществующего пользователя')
    def test_login_with_invalid_data(self, create_user):
        payload = {
            "email": create_user[0],
            "name": create_user[2]
        }
        response = requests.post(Data.URL+LOGIN, data=payload)

        assert response.status_code == 401
        assert response.json()['success'] is False
