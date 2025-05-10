import allure
import requests

from data.handlers import Urls, Handlers
from data.ingredients_data import Ingredient

@allure.suite("Получение доступных заказов по пользователю")
class TestGetOrderUser:

    @allure.description("Авторизованный пользователь получает список заказов")
    @allure.title("Получение доступных заказов авторизованного пользователя")
    def test_get_order_user_with_auth(self, create_user):
        token = {'Authorization': create_user[3]}
        with allure.step('Создание заказа для пользователя'):
            requests_create_order = requests.post(f"{Urls.MAIN_URL}{Handlers.MAKE_ORDER}", headers=token, data=Ingredient.correct_ingredients_data)
        with allure.step('Получение заказов для авторизованного пользователя'):
            response_get_order = requests.get(f"{Urls.MAIN_URL}{Handlers.GET_ORDERS}", headers=token)
        with allure.step('Проверка статуса и номера заказа совпадают'):
            assert response_get_order.status_code == 200
            assert response_get_order.json()['orders'][0]['number'] == requests_create_order.json()['order']['number']


    @allure.description("Некорректный запрос, если пользователь не авторизовался")
    @allure.title("Получение заказов без авторизации")
    def test_get_order_user_not_auth(self):
        with allure.step('Отправка запроса без авторизации'):
            r = requests.get(f"{Urls.MAIN_URL}{Handlers.GET_ORDERS}")
        with allure.step('Проверка сообщения об ошибке'):
            assert r.status_code == 401
            assert r.json()['message'] == "You should be authorised"
