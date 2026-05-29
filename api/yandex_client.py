import logging
import allure
import requests
from pydantic import BaseModel, Field
from config import settings

logger = logging.getLogger(__name__)


# =====================================================================
# 1. СТРОКОВЫЕ ШАБЛОНЫ ЭНДПОИНТОВ (Устранение хардкода по ТЗ D4)
# =====================================================================
class YandexDiskEndpoints:
    DISK_ROOT = "/v1/disk/"
    RESOURCES = "/v1/disk/resources"
    RESTORE = "/v1/disk/trash/resources/restore"


# =====================================================================
# 2. PYDANTIC МОДЕЛИ ВАЛИДАЦИИ (Защита от Bad practices)
# =====================================================================
class UserSchema(BaseModel):
    login: str
    display_name: str


class DiskResponseSchema(BaseModel):
    """Схема для информации о диске"""
    user: UserSchema
    total_space: int = Field(default=0)
    used_space: int = Field(default=0)


class FolderLinkSchema(BaseModel):
    """Схема для успешных ответов (201 Created) при создании/восстановлении"""
    href: str
    method: str
    templated: bool = Field(default=False)


class ErrorResponseSchema(BaseModel):
    """Схема для валидации любых ошибок API (401, 404, 409)"""
    error: str
    description: str
    message: str


# =====================================================================
# 3. API-КЛИЕНТ
# =====================================================================
class YandexDiskClient:
    def __init__(self, token=None):
        self.base_url = settings.base_url
        self.session = requests.Session()

        if token:
            self.session.headers.update({"Authorization": f"OAuth {token}"})

    def _send_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info(f"Request: {method} {url} | Params: {kwargs.get('params')}")

        with allure.step(f"{method} {endpoint}"):
            response = self.session.request(method, url, **kwargs)
            return response

    @allure.step("Получить информацию о диске")
    def get_disk_info(self) -> requests.Response:
        return self._send_request("GET", YandexDiskEndpoints.DISK_ROOT)

    @allure.step("Создать папку")
    def create_folder(self, path: str) -> requests.Response:
        """PUT /v1/disk/resources?path={path}"""
        return self._send_request("PUT", YandexDiskEndpoints.RESOURCES, params={"path": path})

    @allure.step("Удалить папку")
    def delete_folder(self, path: str) -> requests.Response:
        """DELETE /v1/disk/resources?path={path}"""
        return self._send_request("DELETE", YandexDiskEndpoints.RESOURCES, params={"path": path})

    @allure.step("Восстановить папку из корзины")
    def restore_folder(self, path: str) -> requests.Response:
        """PUT /v1/disk/trash/resources/restore?path={path}"""
        return self._send_request("PUT", YandexDiskEndpoints.RESTORE, params={"path": path})

    @allure.step("Получить содержимое корзины")
    def get_trash_contents(self) -> requests.Response:
        """GET /v1/disk/trash/resources"""
        return self._send_request("GET", "/v1/disk/trash/resources")