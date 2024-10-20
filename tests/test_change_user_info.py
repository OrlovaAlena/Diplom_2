import allure
import requests

from src.api_requests import delete_user
from src.data import Data
from src.endpoints import LOGIN, USER


class TestUserInfo:

    @allure.title('Изменение данных авторизованного пользователя')
    def test_change_authorized_user_data(self, create_user):
        payload = {
            "email": create_user[0],
            "password": create_user[1],
            "name": create_user[2]
        }
        requests.post(Data.URL + LOGIN, data=payload)
        token = create_user[3]

        changed_payload = {
            "email": create_user[0] + '1',
            "password": create_user[1] + '1',
            "name": create_user[2] + '1'
        }
        change_user = requests.patch(Data.URL + USER, data=changed_payload, headers={'Authorization': f'{token}'})

        assert change_user.status_code == 200
        assert change_user.json()['user']['email'] == changed_payload['email']
        assert change_user.json()['user']['name'] == changed_payload['name']

        delete_user(token)

    @allure.title('Изменение данных неавторизованного пользователя')
    def test_change_unauthorized_user_data(self, create_user):
        payload = {
            "email": create_user[0],
            "password": create_user[1],
            "name": create_user[2]
        }
        change_user_data = requests.patch(Data.URL + USER, data=payload)

        assert change_user_data.status_code == 401
        assert change_user_data.json()['message'] == Data.AUTHORIZE_ERROR

