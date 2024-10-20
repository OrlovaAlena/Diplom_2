import allure
import requests

from src.api_requests import delete_user
from src.data import Data
from src.endpoints import LOGIN, ORDERS


class TestCreateOrder:

    @allure.title('Создание заказа с авторизацией')
    def test_create_order_with_authorization(self, create_user):
        payload = {
            "email": create_user[0],
            "password": create_user[1],
            "name": create_user[2]
        }
        token = create_user[3]
        requests.post(Data.URL + LOGIN, data=payload)

        data = {
            "ingredients": [Data.BUN, Data.FILLING]
        }
        response = requests.post(Data.URL + ORDERS, data=data, headers={'Authorization': f'{token}'})

        assert response.status_code == 200
        assert response.json()['name'] == Data.BURGER_NAME

        delete_user(token)

    @allure.title('Создание заказа без авторизации')
    def test_create_order_without_authorization(self):
        data = {
            "ingredients": [Data.BUN, Data.FILLING]
        }
        response = requests.post(Data.URL + ORDERS, data=data)

        assert response.status_code == 200

    @allure.title('Создание заказа c невалидным ингредиентом')
    def test_create_order_with_invalid_data(self):
        data = {
            "ingredients": [Data.INVALID_INGREDIENT]
        }
        response = requests.post(Data.URL + ORDERS, data=data)

        assert response.status_code == 500


    @allure.title('Создание заказа без ингредиента')
    def test_create_order_without_data(self, create_user):
        data = {
            "ingredients": ""
        }
        response = requests.post(Data.URL + ORDERS, data=data)

        assert response.status_code == 400
        assert response.json()['message'] == Data.INGREDIENT_ERROR

    @allure.title('Получение заказов авторизованного пользователя')
    def test_get_orders_authorized_user(self, create_user):
        payload = {
            "email": create_user[0],
            "password": create_user[1],
            "name": create_user[2]
        }
        token = create_user[3]
        requests.post(Data.URL + LOGIN, data=payload)

        data = {
            "ingredients": [Data.BUN]
        }
        requests.post(Data.URL + ORDERS, data=data, headers={'Authorization': f'{token}'})
        response = requests.get(Data.URL + ORDERS, headers={'Authorization': f'{token}'})

        assert response.status_code == 200
        assert len(response.json()['orders']) == 1

    @allure.title('Получение заказов без авторизции')
    def test_get_orders_unauthorized_user(self):
        response = requests.get(Data.URL + ORDERS)

        assert response.status_code == 401
        assert response.json()['message'] == Data.AUTHORIZE_ERROR
