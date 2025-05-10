import allure
import requests

from data.handlers import Urls, Handlers
from data.user_data import User


@allure.suite('Авторизация пользователя')
class Testlogin:

    @allure.description('При авторизации под существующим пользователем, происходит успешный вход')
    @allure.title('Авторизация под существующим пользователем')
    def test_login_user(self):
        with allure.step('Отправка POST-запрос с правильными данными для входа'):
            response = requests.post(f'{Urls.MAIN_URL}{Handlers.LOGIN}', data=User.data_correct)
        with allure.step('Проверка успешного входа'):
            assert response.status_code == 200
            assert response.json().get('success') == True

    @allure.description('При вводе некорректных логина или пароля срабатывает ошибка')
    @allure.title('Авторизация с неправильными данными')
    def test_login_user_error(self):
        with allure.step('Отправка POST-запрос с неправильными данными'):
            response = requests.post(f'{Urls.MAIN_URL}{Handlers.LOGIN}', data=User.data_negative)
        with allure.step('Проверка сообщения об ошибке'):
            assert response.status_code == 401
            assert response.json().get('success') == False
