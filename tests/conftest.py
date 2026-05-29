import uuid
import pytest
from api.yandex_client import YandexDiskClient
from config import settings


@pytest.fixture
def yandex_client():
    """Фикстура для успешных тестов (с валидным токеном)"""
    assert settings.yandex_token, "Ошибка: Не задан YANDEX_TOKEN в настройках"

    client = YandexDiskClient(token=settings.yandex_token)
    yield client
    client.session.close()


@pytest.fixture
def unauthorized_client():
    """Фикстура для негативных тестов без токена"""
    client = YandexDiskClient(token=None)
    yield client
    client.session.close()


@pytest.fixture
def unique_folder_name():
    """Генерация уникального имени папки для изоляции тестов"""
    return f"sdet_folder_{uuid.uuid4().hex[:8]}"


@pytest.fixture
def auto_cleanup_folder(yandex_client, unique_folder_name):
    """Фикстура автоматической очистки папки после теста (TearDown)"""
    yield unique_folder_name
    # Гарантированное удаление папки после выполнения теста, даже если тест упал
    yandex_client.delete_folder(path=unique_folder_name)