import logging
import allure
import requests
from pydantic import BaseModel, Field
from config import settings

logger = logging.getLogger(__name__)

# =====================================================================
# 1. СТРОКОВЫЕ ШАБЛОНЫ ЭНДПОИНТОВ (Вынесено по рекомендации ментора)
# =====================================================================
class YandexDiskEndpoints:
    # Базовый корень для работы с диском.
    # Если в будущем понадобится передавать параметры, сможем использовать .format()
    DISK_ROOT = "/v1/disk/"


# =====================================================================
# 2. PYDANTIC МОДЕЛИ ВАЛИДАЦИИ (Внедрено по рекомендации ментора)
# =====================================================================
class UserSchema(BaseModel):
    login: str
    display_name: str

class DiskResponseSchema(BaseModel):
    """Схема для валидации успешного ответа 200 OK"""
    user: UserSchema
    total_space: int = Field(default=0)
    used_space: int = Field(default=0)

class ErrorResponseSchema(BaseModel):
    """Схема для валидации ошибки 401 Unauthorized"""
    error: str
    description: str
    message: str


# =====================================================================
# 3. ОБНОВЛЕННЫЙ API-КЛИЕНТ
# =====================================================================
class YandexDiskClient:
    def __init__(self, token=None):
        self.base_url = settings.base_url
        self.session = requests.Session()

        # Если токен передан, добавляем заголовок авторизации
        if token:
            self.session.headers.update({"Authorization": f"OAuth {token}"})

    def _send_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info(f"Request: {method} {url}")

        with allure.step(f"{method} {endpoint}"):
            # Для тест-кейса №2: если токен не был передан в __init__,
            # сессия отправит запрос без заголовка Authorization
            response = self.session.request(method, url, **kwargs)
            return response

    @allure.step("Получить информацию о диске")
    def get_disk_info(self) -> requests.Response:
        # Используем константу вместо хардкода строки
        return self._send_request("GET", YandexDiskEndpoints.DISK_ROOT)