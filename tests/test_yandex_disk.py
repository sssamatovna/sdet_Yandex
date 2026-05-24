import allure
from config import settings
from helpers.allure_helpers import attach_api_response, attach_validation_result

# Импортируем схемы валидации, которые мы добавили в клиентский модуль
from api.yandex_client import DiskResponseSchema, ErrorResponseSchema


@allure.epic("Yandex Disk API")
@allure.feature("Получение информации о диске")
@allure.story("Успешное получение данных")
@allure.title("ТС-01 Авторизация с валидным токеном")
@allure.description("Проверка получения данных авторизированного пользователя")
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("smoke", "auth", "positive")
def test_tc1_auth_valid_token(yandex_client):
    with allure.step("Отправить GET запрос по адресу v1/disk/"):
        response = yandex_client.get_disk_info()
        attach_api_response(response, expected_status=200)

    with allure.step("Проверить статус-код ответа"):
        assert (
                response.status_code == 200
        ), f"Ожидался 200, получен {response.status_code}"

    with allure.step("Валидировать структуру ответа через Pydantic"):
        # Строгая проверка типов данных по требованию ментора
        parsed_data = DiskResponseSchema(**response.json())

    with allure.step("Проверить данные пользователя"):
        attach_validation_result("Login", settings.yandex_login, parsed_data.user.login)
        assert (
                parsed_data.user.login == settings.yandex_login
        ), f"Login ожидался '{settings.yandex_login}', получен '{parsed_data.user.login}'"

        attach_validation_result(
            "Display Name", settings.yandex_display_name, parsed_data.user.display_name
        )
        assert (
                parsed_data.user.display_name == settings.yandex_display_name
        ), f"Name ожидался '{settings.yandex_display_name}', получен '{parsed_data.user.display_name}'"


@allure.epic("Yandex Disk API")
@allure.feature("Получение информации о диске")
@allure.story("Обработка ошибок доступа")
@allure.title("ТС-02 Авторизация без токена")
@allure.description(
    "Проверка получения 401 ошибки при запросе без заголовка Authorization"
)
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("security", "auth", "negative")
# Используем чистую фикстуру unauthorized_client вместо создания объекта вручную
def test_tc2_auth_missing_token(unauthorized_client):
    with allure.step("Отправить GET запрос по адресу v1/disk/ без передачи токена"):
        response = unauthorized_client.get_disk_info()
        attach_api_response(response, expected_status=401)

    with allure.step("Проверить статус-код ответа"):
        assert (
                response.status_code == 401
        ), f"Ожидался 401, получен {response.status_code}"

    with allure.step("Валидировать структуру ошибки через Pydantic"):
        # Проверяем, что API вернул ровно те поля, что описаны в схеме (error, description, message)
        parsed_error = ErrorResponseSchema(**response.json())

    with allure.step("Проверить структуру и тип ошибки"):
        attach_validation_result("Error", "UnauthorizedError", parsed_error.error)
        assert (
                parsed_error.error == "UnauthorizedError"
        ), f"Ожидался 'UnauthorizedError', получен '{parsed_error.error}' "

        # Сами проверки "in result" больше не нужны, так как Pydantic
        # уже гарантировал наличие этих полей при создании parsed_error.
        assert parsed_error.description is not None, "Поле 'description' пустое"
        assert parsed_error.message is not None, "Поле 'message' пустое"