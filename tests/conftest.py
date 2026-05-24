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
    """Фикстура для негативных тестов (без передачи токена)"""
    # Создаем клиент со значением token=None
    client = YandexDiskClient(token=None)
    yield client
    client.session.close()