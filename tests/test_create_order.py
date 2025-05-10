import allure
import requests


from data.handlers import Urls, Handlers
from data.ingredients_data import Ingredient


@allure.suite("Создание заказа")
class TestCreateOrder:

    @allure.description("Создание заказа авторизованным пользователем")
    @allure.title("Создание заказа авторизованным пользователем")
    def test_create_order_with_auth(self, create_user):
        token = {'Authorization': create_user[3]}
        with allure.step('Отправка POST-запрос для создания заказа с авторизацией'):
            r = requests.post(f"{Urls.MAIN_URL}{Handlers.MAKE_ORDER}", headers=token, data=Ingredient.correct_ingredients_data)
        with allure.step('Проверка ответа о успешном создании заказа'):
            assert r.status_code == 200
            assert r.json().get("success") is True

    @allure.description("Создание заказа не авторизованным пользователем")
    @allure.title("Создание заказа без авторизации")
    def test_create_order_not_auth(self):
        with allure.step('Отправка POST-запрос без авторизационных данных'):
            r = requests.post(f"{Urls.MAIN_URL}{Handlers.MAKE_ORDER}")
        with allure.step('Проверка ответа о успешном создании заказа'):
            assert r.status_code == 200
            assert r.json().get("success") is True

    @allure.description("Создание заказа без ингредиентов должно возвращать ошибку")
    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_with_ingridient(self):
        with allure.step('Отправка POST-запрос без ингредиентов'):
            r = requests.post(f"{Urls.MAIN_URL}{Handlers.MAKE_ORDER}")
        with allure.step('Проверка сообщения об ошибке'):
            assert r.status_code == 400
            assert r.json()['message'] == "Ingredient ids must be provided"

    @allure.description("Создание заказа с невалидным хешем ингредиента должно возвращать ошибку сервера")
    @allure.title("Создание заказа с невалидным хешем ингредиента")
    def test_create_order_invalid_hash_ingridient(self):
        with allure.step('Отправка POST-запрос с некорректным ингредиентом'):
            response = requests.post(Urls.MAIN_URL + Handlers.MAKE_ORDER, headers=Handlers.headers, json=Ingredient.incorrect_ingredients_data)
        with allure.step('Проверка ответа о внутренней ошибке сервера'):
            assert response.status_code == 500
            assert 'Internal Server Error' in response.text
