# ☁️ Yandex Disk API Automation Tests

**Проект:** Задание D3 - Автотесты REST
**Автор:** Ильясова Аделя  
**Стек:** Python 3.10, Pytest, Allure
**Дата:** Май 2026

---

## 📋 Описание проекта

Проект автоматизированного тестирования REST API Яндекс.Диска.
Включает проверки авторизации (позитивные и негативные сценарии) и получения информации о диске.

## 🛠️ Технологии

| Технология           | Назначение |
|----------------------|------------|
| **Python 3.10**      | Язык программирования |
| **Pytest**           | Фреймворк для тестирования |
| **Requests**         | HTTP клиент для API запросов |
| **Pydantic Settings** | Управление конфигурацией с валидацией |
| **Allure**           | Генерация красивых HTML отчётов |
| 

---
## 🚀 Установка и настройка

### 1. Клонирование репозитория
```bash
git clone https://github.com/sssamatovna/sdet_Yandex.git
cd sdet_Yandex
```

### 2. Создание виртуального окружения
Рекомендуется использовать виртуальное окружение для изоляции зависимостей.

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Конфигурация (.env)
Создайте файл `.env` в корне проекта и заполните его вашими данными (используйте `.env.template` как пример):

```ini
# Base URL API Яндекс.Диска
BASE_URL=https://cloud-api.yandex.net

# Ваш OAuth токен (получить на https://yandex.ru/dev/disk/poligon/ )
YANDEX_TOKEN=y0_AgAAAA...

# Ожидаемые данные пользователя для проверок
YANDEX_LOGIN=your_login
YANDEX_DISPLAY_NAME=your_display_name
```

---

## ▶️ Запуск тестов

### Простой запуск
```bash
pytest
```

### Запуск с генерацией отчета Allure
```bash
pytest --alluredir=allure-results
```

### Просмотр отчета
Чтобы открыть отчет в браузере, необходима утилита Allure Commandline:
```bash
allure serve allure-results
```

---

### Скриншоты

<details>
  <summary><strong>📈 Обзор выполнения тестов (кликни, чтобы развернуть)</strong></summary>
  
  ![Обзор отчета Allure](screenshot\allure_overview.png)
</details>

<details>
  <summary><strong>📄 Детализация 1 тест-кейса (кликни, чтобы развернуть)</strong></summary>
  
  ![Детализация шагов теста](screenshot\allure_tc01.png)
</details>

<details>
  <summary><strong>📄 GET запрос через postman для первого тест кейса(кликни, чтобы развернуть)</strong></summary>
  
  ![Детализация шагов теста](screenshot\postman_tc01.png)
</details>

<details>
  <summary><strong>📄 Детализация 2 тест-кейса (кликни, чтобы развернуть)</strong></summary>
  
  ![Детализация шагов теста](screenshot\allure_tc02.png)
</details>

<details>
  <summary><strong>📄 GET запрос через postman для второго тест кейса (кликни, чтобы развернуть)</strong></summary>
  
  ![Детализация шагов теста](screenshot\postman_tc02.png)
</details>

