import allure
import pytest
from helpers.allure_helpers import attach_api_response, attach_validation_result
from api.yandex_client import FolderLinkSchema, ErrorResponseSchema


@allure.epic("Yandex Disk API")
@allure.feature("Управление папками ресурса")
class TestYandexDiskFolders:

    @allure.story("Позитивные сценарии")
    @allure.title("ТС-01 Создание новой папки")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "folder", "positive")
    def test_tc1_create_folder(self, yandex_client, auto_cleanup_folder):
        folder_name = auto_cleanup_folder

        with allure.step(f"Отправить PUT запрос на создание папки '{folder_name}'"):
            response = yandex_client.create_folder(path=folder_name)
            attach_api_response(response, expected_status=201)

        with allure.step("Проверить статус-код ответа"):
            assert response.status_code == 201, f"Ожидался 201, получен {response.status_code}"

        with allure.step("Валидировать структуру ответа через Pydantic"):
            parsed_data = FolderLinkSchema(**response.json())
            assert parsed_data.method == "GET", "Ожидался метод GET для созданного ресурса"

    @allure.story("Позитивные сценарии")
    @allure.title("ТС-02 Удаление папки (Перемещение в корзину)")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "folder", "positive")
    def test_tc2_delete_folder(self, yandex_client, unique_folder_name):
        folder_name = unique_folder_name

        with allure.step(f"Предусловие: Создать папку '{folder_name}'"):
            yandex_client.create_folder(path=folder_name)

        with allure.step(f"Отправить DELETE запрос для папки '{folder_name}'"):
            response = yandex_client.delete_folder(path=folder_name)
            attach_api_response(response, expected_status=204)

        with allure.step("Проверить статус-код ответа"):
            assert response.status_code == 204, f"Ожидался 204, получен {response.status_code}"

    @allure.story("Позитивные сценарии")
    @allure.title("ТС-03 Восстановление папки из корзины")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "folder", "positive")
    def test_tc3_restore_folder(self, yandex_client, auto_cleanup_folder):
        folder_name = auto_cleanup_folder

        with allure.step(f"Предусловие: Создать и удалить папку '{folder_name}'"):
            yandex_client.create_folder(path=folder_name)
            yandex_client.delete_folder(path=folder_name)

        with allure.step("Динамически найти точный путь папки в корзине"):
            trash_response = yandex_client.get_trash_contents()
            assert trash_response.status_code == 200, "Не удалось получить содержимое корзины"

            # Ищем наш объект среди удаленных элементов
            items = trash_response.json().get("_embedded", {}).get("items", [])
            exact_trash_path = None
            for item in items:
                if item.get("name") == folder_name:
                    exact_trash_path = item.get("path")
                    break

            # Если вдруг в корзине не нашли (капризы кэша API), используем fallback-вариант
            if not exact_trash_path:
                exact_trash_path = f"trash:/{folder_name}"

        with allure.step(f"Отправить PUT запрос на восстановление из '{exact_trash_path}'"):
            response = yandex_client.restore_folder(path=exact_trash_path)
            attach_api_response(response, expected_status=201)

        with allure.step("Проверить статус-код ответа"):
            assert response.status_code == 201, f"Ожидался 201, получен {response.status_code}"

        with allure.step("Валидировать структуру ответа восстановления"):
            parsed_data = FolderLinkSchema(**response.json())
            assert parsed_data.href is not None

    @allure.story("Негативные сценарии")
    @allure.title("ТС-04 Создание папки с уже существующим именем")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "folder", "negative")
    def test_tc4_create_existing_folder(self, yandex_client, auto_cleanup_folder):
        folder_name = auto_cleanup_folder

        with allure.step(f"Предусловие: Инициализировать папку '{folder_name}'"):
            yandex_client.create_folder(path=folder_name)

        with allure.step(f"Повторно отправить PUT запрос для папки '{folder_name}'"):
            response = yandex_client.create_folder(path=folder_name)
            attach_api_response(response, expected_status=409)

        with allure.step("Проверить статус-код ответа и Pydantic-структуру ошибки"):
            assert response.status_code == 409, f"Ожидался 409, получен {response.status_code}"
            parsed_error = ErrorResponseSchema(**response.json())

            # ТЗ-Исправление: Яндекс возвращает именно 'DiskPathPointsToExistentDirectoryError'
            attach_validation_result("Error Type", "DiskPathPointsToExistentDirectoryError", parsed_error.error)
            assert parsed_error.error == "DiskPathPointsToExistentDirectoryError"

    @allure.story("Негативные сценарии")
    @allure.title("ТС-05 Удаление несуществующей папки")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "folder", "negative")
    def test_tc5_delete_non_existent_folder(self, yandex_client, unique_folder_name):
        invalid_folder = f"{unique_folder_name}_not_exist"

        with allure.step(f"Отправить DELETE запрос для несуществующей папки '{invalid_folder}'"):
            response = yandex_client.delete_folder(path=invalid_folder)
            attach_api_response(response, expected_status=404)

        with allure.step("Проверить статус-код ответа и текст ошибки"):
            assert response.status_code == 404, f"Ожидался 404, получен {response.status_code}"
            parsed_error = ErrorResponseSchema(**response.json())
            assert parsed_error.error in ["DiskNotFoundError", "NotFoundError"]

    @allure.story("Негативные сценарии")
    @allure.title("ТС-06 Восстановление несуществующего ресурса из корзины")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "folder", "negative")
    def test_tc6_restore_non_existent_folder(self, yandex_client, unique_folder_name):
        # Передаем фейковый путь в корзине
        invalid_folder = f"trash:/{unique_folder_name}_trash_fake"

        with allure.step(f"Отправить PUT запрос на восстановление отсутствующей папки '{invalid_folder}'"):
            response = yandex_client.restore_folder(path=invalid_folder)
            attach_api_response(response, expected_status=404)

        with allure.step("Проверить статус-код ответа и тип ошибки Pydantic"):
            assert response.status_code == 404, f"Ожидался 404, получен {response.status_code}"
            parsed_error = ErrorResponseSchema(**response.json())

            # ТЗ-Исправление: Расширили список валидных ошибок под 'DiskNotFoundError'
            assert parsed_error.error in ["TrashNotFoundError", "NotFoundError", "DiskNotFoundError"]