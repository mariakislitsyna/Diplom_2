import allure
import requests

from data.handlers import Urls, Handlers
from data.user_data import User


@allure.suite('Изменение данных пользовователя')
class TestChangingUserData:

    @allure.description("При попытке сменить email у авторизованного пользователя, изменение данных происходит успешно")
    @allure.title("Успешное изменение email авторизованного пользователя")
    def test_changing_user_email_with_auth(self, create_user):
        payload = {'email': User.create_data_user()["email"]}
        token = {'Authorization': create_user[3]}
        with allure.step('Отправка PATCH-запрос на изменение email'):
            r = requests.patch(f"{Urls.MAIN_URL}{Handlers.CHANGE_USER_DATA}", headers=token, data=payload)
        with allure.step('Проверка статуса ответа и соответствия email'):
            assert r.status_code == 200
            assert r.json()['user']['email'] == payload["email"]

    @allure.description("При попытке сменить password у авторизованного пользователя, изменение данных происходит успешно")
    @allure.title("Успешное изменение password авторизованного пользователя")
    def test_changing_user_password_with_auth(self, create_user):
        payload = {'password': User.create_data_user()["password"]}
        token = {'Authorization': create_user[3]}
        with allure.step('Отправка PATCH-запрос на изменение пароля'):
            r = requests.patch(f"{Urls.MAIN_URL}{Handlers.CHANGE_USER_DATA}", headers=token, data=payload)
        with allure.step('Проверка ответа о успешности'):
            assert r.status_code == 200
            assert r.json().get("success") is True

    @allure.description("При попытке сменить name у авторизованного пользователя, изменение данных происходит успешно")
    @allure.title("Успешное изменение name авторизованного пользователя")
    def test_changing_user_name_with_auth(self, create_user):
        payload = {'name': User.create_data_user()["name"]}
        token = {'Authorization': create_user[3]}
        with allure.step('Отправка PATCH-запрос на изменение имени'):
            r = requests.patch(f"{Urls.MAIN_URL}{Handlers.CHANGE_USER_DATA}", headers=token, data=payload)
        with allure.step('Проверка статуса ответа и соответсвия имени'):
            assert r.status_code == 200
            assert r.json()['user']['name'] == payload["name"]

    @allure.description("При попытке смены данных пользователя без авторизации, возвращает alert")
    @allure.title("Изменение данных пользователя без авторизации")
    def test_changing_user_data_not_auth(self):
        with allure.step('Отправка PATCH-запрос без авторизационных заголовков'):
            r = requests.patch(f"{Urls.MAIN_URL}{Handlers.CHANGE_USER_DATA}", data=User.create_data_user())
        with allure.step('Проверка статуса и сообщения об ошибке'):
            assert r.status_code == 401
            assert r.json()['message'] == 'You should be authorised'