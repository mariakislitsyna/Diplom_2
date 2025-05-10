import pytest
import allure
import requests

from data.handlers import Urls, Handlers
from data.user_data import User


@allure.suite('Создание пользователя')
class TestCreateUser:

    @allure.description('Создание нового пользователя')
    @allure.title('Создание нового пользователя')
    def test_create_new_user_success(self):
        with allure.step('Отправка POST-запрос для создания пользователя'):
            response = requests.post(f'{Urls.MAIN_URL}{Handlers.CREATE_USER}', data=User.create_data_user())
        with allure.step('Проверка успешности создания пользователя'):
            assert response.status_code == 200
            assert response.json()["success"] is True

    @allure.description('При создании дублирующего пользователя срабатывает alert')
    @allure.title('Создание пользователя, который уже есть в системе')
    def test_create_double_user_error(self):
        with allure.step('Отправка POST-запрос для создания повторяющегося пользователя'):
            response = requests.post(f'{Urls.MAIN_URL}{Handlers.CREATE_USER}', data=User.data_double)
        with allure.step('Проверка сообщения об ошибке о существовании пользователя'):
            assert response.status_code == 403
            assert 'User already exists' in response.text

    @allure.description('При создании пользователя с некорректными данными срабатывает alert')
    @allure.title('Создание пользователя с некорректными или неполными данными')
    @pytest.mark.parametrize("user_data", [User.data_without_email, User.data_without_password, User.data_without_name])
    def test_create_user_incorrect_data(self, user_data):
        with allure.step('Отправка POST-запрос с некорректными данными'):
            response = requests.post(f'{Urls.MAIN_URL}{Handlers.CREATE_USER}', data=user_data)
        with allure.step('Проверка сообщения об ошибке'):
            assert response.status_code == 403
            assert 'Email, password and name are required fields' in response.text
