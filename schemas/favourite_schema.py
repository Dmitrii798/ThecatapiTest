# schemas/__init__.py  (пустой файл)

# schemas/favourite_schema.py
import allure


def is_valid_favourite_schema(data: dict) -> bool:
    """
    Проверяет, что ответ соответствует схеме Favourite.

    Ожидаемые поля:
    - id: int
    - image_id: str
    - sub_id: str or null
    - created_at: str (ISO дата)
    """
    if not isinstance(data, dict):
        return False

    required_keys = ["id", "image_id", "sub_id", "created_at"]
    if not all(key in data for key in required_keys):
        return False

    # Проверяем типы
    if not isinstance(data["id"], int):
        return False
    if not isinstance(data["image_id"], str):
        return False
    if data["sub_id"] is not None and not isinstance(data["sub_id"], str):
        return False
    if not isinstance(data["created_at"], str):
        return False

    return True


def is_valid_favourites_list_schema(data: list) -> bool:
    """Проверяет, что ответ — список объектов Favourite."""
    if not isinstance(data, list):
        return False
    if len(data) == 0:
        return True
    return all(is_valid_favourite_schema(item) for item in data)


def check_favourite_schema(response) -> None:
    """Проверка схемы ответа при создании/получении одного favourite."""
    with allure.step("Check Favourite response schema"):
        print("   🔍 Checking Favourite schema...")
        data = response.json()
        assert is_valid_favourite_schema(data), f"Invalid schema: {data}"
        print(f"   ✅ Favourite schema valid: {list(data.keys())}")
        allure.attach(
            str(data),
            name="Validated schema",
            attachment_type=allure.attachment_type.JSON
        )


def check_favourites_list_schema(response) -> None:
    """Проверка схемы ответа при получении списка favourites."""
    with allure.step("Check Favourites list response schema"):
        print("   🔍 Checking Favourites list schema...")
        data = response.json()
        assert is_valid_favourites_list_schema(data), f"Invalid schema: {data}"
        print(f"   ✅ List schema valid: {len(data)} items")
        allure.attach(
            f"Validated list with {len(data)} items",
            name="Validated schema",
            attachment_type=allure.attachment_type.TEXT
        )
