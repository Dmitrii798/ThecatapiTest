# 🐱 TheCatAPI Test Automation

Автотесты для API [TheCatAPI](https://developers.thecatapi.com/) с использованием **Python**, **Pytest**, **Requests** и
**Allure**.

[![API Tests](https://github.com/ВАШ_ЛОГИН/ThecatapiTest/actions/workflows/tests.yml/badge.svg)](https://github.com/ВАШ_ЛОГИН/ThecatapiTest/actions/workflows/tests.yml)

---

## 📋 Описание

Проект содержит **13 автотестов**, покрывающих все методы вкладки **Favourites** из TheCatAPI:

| №  | Проверка                             | Файл                      |
|----|--------------------------------------|---------------------------|
| 1  | Фильтр по количеству картинок        | `test_parameters.py`      |
| 2  | Сортировка в обратном порядке (DESC) | `test_parameters.py`      |
| 3  | Фильтр по несуществующему image_id   | `test_parameters.py`      |
| 4  | Неправильный Content-Type            | `test_header.py`          |
| 5  | Изменение регистра хедера            | `test_authentication.py`  |
| 6  | Без аутентификации                   | `test_authentication.py`  |
| 7  | Дублирующийся image_id               | `test_parameters.py`      |
| 8  | Неправильный тип sub_id              | `test_parameters.py`      |
| 9  | Скачать валидный JPEG                | `test_header.py`          |
| 10 | Добавить favourite                   | `test_favourites_crud.py` |
| 11 | Добавить и удалить favourite         | `test_favourites_crud.py` |

---

## 🛠️ Технологии

- **Python 3.11+**
- **Pytest** — фреймворк для тестирования
- **Requests** — HTTP-клиент
- **Allure** — генерация отчётов
- **python-dotenv** — хранение API-ключа

---

## 🚀 Установка

### 1. Клонируй репозиторий

```bash
git clone https://github.com/ВАШ_ЛОГИН/ThecatapiTest.git
cd ThecatapiTest
```

### 2. Создай виртуальное окружение

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### 3. Установи зависимости

```bash
pip install -r requirements.txt
```

### 4. Получи API-ключ

Зарегистрируйся на [TheCatAPI](https://thecatapi.com/) и получи бесплатный API-ключ.

### 5. Создай `.env` файл

```ini
THE_CAT_API_KEY = твой_api_ключ_здесь
```

---

## 🏃 Запуск тестов

### Все тесты

```bash
pytest -v -s --alluredir=results
```

### Конкретный файл

```bash
pytest test_parameters.py -v -s --alluredir=results
```

### Конкретный тест

```bash
pytest test_parameters.py::TestParameters::test_favourites_limit_50_order_desc -v -s
```

---

## 📊 Отчёт Allure

### Просмотр отчёта (локально)

```bash
allure serve results
```

### Генерация HTML-отчёта

```bash
allure generate results -o allure-report --clean
allure open allure-report
```

---

## 🧪 Структура тестов

### `test_authentication.py`

- `test_endpoints_without_auth` — проверка 401 без API-ключа
- `test_api_key_header_case_insensitive` — регистронезависимость хедера

### `test_favourites_crud.py`

- `test_add_favourite_and_verify` — создание + проверка появления
- `test_add_and_delete_favourite` — создание + удаление

### `test_header.py`

- `test_add_favourite_wrong_content_type` — ошибка при text/plain
- `test_download_image_is_valid_jpeg` — валидация JPEG

### `test_parameters.py`

- `test_favourites_limit_50_order_desc` — фильтр + сортировка
- `test_invalid_sub_id_type` — параметризованный тест (4 параметра)
- `test_filter_by_nonexistent_image_id` — фильтр по фейковому ID
- `test_add_duplicate_image_id` — дубликат

---

## 📈 CI/CD

Проект использует **GitHub Actions** для автозапуска тестов:

- При каждом **push** в `main`/`master`
- При каждом **pull request**
- Вручную через **workflow_dispatch**

Отчёт Allure публикуется на **GitHub Pages**.

---

## 📂 Структура проекта

```
ThecatapiTest/
├── .github/workflows/tests.yml    # CI/CD
├── schemas/                       # Валидация схем
├── helpers/                       # Утилиты
├── checkers.py                    # Функции проверок
├── conftest.py                    # Фикстуры
├── config.py                      # Константы
├── test_*.py                      # Тесты
└── requirements.txt               # Зависимости
```

---

## 📝 Лицензия

MIT

---

## 👤 Автор

**Твоё Имя**

- GitHub: [@ВАШ_ЛОГИН](https://github.com/ВАШ_ЛОГИН)