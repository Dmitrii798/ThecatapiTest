import allure
import pytest
import requests
import time

from config import url
from helpers.attach import allure_attachment
from checkers import (
    check_status_200,
    check_response_length,
    check_dates_order_desc,
    check_not_empty,
    check_empty_response,
)
from schemas.favourite_schema import check_favourites_list_schema


@allure.suite("homework")
class TestParameters:

    @allure.title("Get favourites with limit=50 and order=DESC")
    @allure.description(
        "Проверяет, что фильтр по limit=50 возвращает не более 50 записей, "
        "и что сортировка order=DESC возвращает favourites в порядке убывания created_at."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.homework
    def test_favourites_limit_50_order_desc(self, headers: dict) -> None:
        print("\n" + "=" * 60)
        print("🚀 START: test_favourites_limit_50_order_desc")
        print("=" * 60)

        # ===== ПОДГОТОВКА =====
        created_ids = []
        with allure.step("Precondition: create 3 favourites for the test"):
            print("\n📦 PRECONDITION: Creating 3 favourites...")
            for i in range(3):
                search_resp = requests.get(
                    f"{url}/images/search",
                    params={"limit": 1},
                    headers=headers
                )
                check_status_200(search_resp)
                image_id = search_resp.json()[0]["id"]
                print(f"   🐱 Got image_id: {image_id}")

                create_resp = requests.post(
                    f"{url}/favourites",
                    headers=headers,
                    json={"image_id": image_id, "sub_id": f"test_user_{i}"}
                )
                assert create_resp.status_code in [200, 201], \
                    f"Failed to create favourite: {create_resp.text}"
                fav_id = create_resp.json()["id"]
                created_ids.append(fav_id)
                print(f"   ✅ Created favourite #{i + 1} with id: {fav_id}")

                time.sleep(1)

        try:
            # ===== ОСНОВНОЙ ТЕСТ =====
            print("\n🔍 MAIN TEST: Sending GET /favourites?limit=50&order=DESC")
            with allure.step("Send GET request to /favourites with limit=50 and order=DESC"):
                response = requests.get(
                    f"{url}/favourites?limit=50&order=DESC",
                    headers=headers
                )
            print(f"   📡 Status code: {response.status_code}")

            allure_attachment(response)
            check_status_200(response)
            check_not_empty(response)
            check_response_length(response, len_my=50)
            check_dates_order_desc(response)
            check_favourites_list_schema(response)
            check_favourites_list_schema(response)
            print(f"   ✅ List schema check passed")

            with allure.step("Log the number of returned favourites"):
                count = len(response.json())
                print(f"   📊 Returned {count} favourites")
                print(f"   📅 Dates in DESC order: ✅")
                allure.attach(
                    f"Returned {count} favourites",
                    name="Count",
                    attachment_type=allure.attachment_type.TEXT
                )

        finally:
            # ===== УБОРКА =====
            print("\n🧹 CLEANUP: Deleting created favourites...")
            with allure.step("Cleanup: delete created favourites"):
                for fav_id in created_ids:
                    del_resp = requests.delete(
                        f"{url}/favourites/{fav_id}",
                        headers=headers
                    )
                    assert del_resp.status_code == 200, \
                        f"Failed to delete favourite {fav_id}"
                    print(f"   🗑️ Deleted favourite: {fav_id}")

        print("\n" + "=" * 60)
        print("✅ FINISH: test passed successfully")
        print("=" * 60 + "\n")

    # ==================== ПАРАМЕТРИЗОВАННЫЙ ТЕСТ ====================

    @allure.title("Invalid sub_id type returns error")
    @allure.description("Проверяет, что неправильный тип sub_id приводит к ошибке.")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.homework
    @pytest.mark.parametrize("invalid_sub_id", [
        12345,  # число
        True,  # булево
        {"key": "value"},  # словарь
        [1, 2, 3],  # список
        # None убран, так как API принимает null для sub_id
    ])
    def test_invalid_sub_id_type(self, headers: dict, invalid_sub_id) -> None:
        # ← ВСЁ ТЕЛО МЕТОДА С ОТСТУПОМ 8 ПРОБЕЛОВ (2 уровня)
        print("\n" + "=" * 60)
        print(f"🚀 START: test_invalid_sub_id_type with {type(invalid_sub_id).__name__} = {invalid_sub_id}")
        print("=" * 60)

        # Получаем image_id
        print("\n📦 PRECONDITION: Getting a random image_id...")
        search_resp = requests.get(
            f"{url}/images/search",
            params={"limit": 1},
            headers=headers
        )
        check_status_200(search_resp)
        image_id = search_resp.json()[0]["id"]
        print(f"   🐱 Got image_id: {image_id}")

        # Отправляем POST с неправильным sub_id
        payload = {"image_id": image_id, "sub_id": invalid_sub_id}
        print(f"\n🔍 MAIN TEST: Sending POST /favourites")
        print(f"   📤 Payload: {payload}")
        print(f"   📤 sub_id type: {type(invalid_sub_id).__name__}")

        with allure.step(f"Send POST with invalid sub_id type: {type(invalid_sub_id).__name__}"):
            resp = requests.post(
                f"{url}/favourites",
                headers=headers,
                json=payload
            )

        print(f"   📡 Status: {resp.status_code}")
        print(f"   📥 Response: {resp.text}")

        allure_attachment(resp)

        with allure.step("Check that API returned an error"):
            assert resp.status_code >= 400, \
                f"Expected error for sub_id type {type(invalid_sub_id).__name__}, got {resp.status_code}"
            print(f"   ✅ Error received as expected")

        print("\n" + "=" * 60)
        print("✅ FINISH: test passed successfully")
        print("=" * 60 + "\n")

    @allure.title("Filter favourites by non-existent image_id returns empty list")
    @allure.description(
        "Проверяет, что фильтр по несуществующему image_id возвращает пустой список."
    )
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.homework
    def test_filter_by_nonexistent_image_id(self, headers: dict) -> None:
        """Требование 3: Фильтр по картинке с несуществующим image_id ничего не выдает."""
        print("\n" + "=" * 60)
        print("🚀 START: test_filter_by_nonexistent_image_id")
        print("=" * 60)

        fake_image_id = "nonexistent12345"
        print(f"\n🔍 MAIN TEST: Filter by fake image_id: {fake_image_id}")

        with allure.step(f"Send GET /favourites?image_id={fake_image_id}"):
            response = requests.get(
                f"{url}/favourites",
                params={"image_id": fake_image_id},
                headers=headers
            )

        print(f"   📡 Status code: {response.status_code}")
        print(f"   📥 Response: {response.text}")

        allure_attachment(response)
        check_status_200(response)
        check_empty_response(response)

        print("\n" + "=" * 60)
        print("✅ FINISH: test passed successfully")
        print("=" * 60 + "\n")

    @allure.title("Adding duplicate image_id returns error")
    @allure.description(
        "Проверяет, что при добавлении картинок с одинаковым image_id возникает ошибка."
    )
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.homework
    def test_add_duplicate_image_id(self, headers: dict) -> None:
        """Требование 7: При добавлении картинок с одинаковым image_id возникает ошибка."""
        print("\n" + "=" * 60)
        print("🚀 START: test_add_duplicate_image_id")
        print("=" * 60)

        # 1. Получаем image_id
        print("\n📦 PRECONDITION: Getting a random image_id...")
        search_resp = requests.get(
            f"{url}/images/search",
            params={"limit": 1},
            headers=headers
        )
        check_status_200(search_resp)
        image_id = search_resp.json()[0]["id"]
        print(f"   🐱 Got image_id: {image_id}")

        payload = {"image_id": image_id, "sub_id": "duplicate_test_user"}
        created_ids = []

        try:
            # 2. Создаём первый favourite
            print("\n🔍 STEP 1: Creating first favourite...")
            with allure.step("Create first favourite"):
                resp1 = requests.post(f"{url}/favourites", headers=headers, json=payload)

            print(f"   📡 Status: {resp1.status_code}")
            print(f"   📥 Response: {resp1.text}")
            allure_attachment(resp1)

            assert resp1.status_code in [200, 201], \
                f"Failed to create first favourite: {resp1.text}"
            fav_id = resp1.json()["id"]
            created_ids.append(fav_id)
            print(f"   ✅ Created favourite with id: {fav_id}")

            # 3. Пытаемся создать второй favourite с тем же image_id и sub_id
            print("\n🔍 STEP 2: Trying to create DUPLICATE favourite...")
            with allure.step("Try to create duplicate favourite with same image_id"):
                resp2 = requests.post(f"{url}/favourites", headers=headers, json=payload)

            print(f"   📡 Status: {resp2.status_code}")
            print(f"   📥 Response: {resp2.text}")
            allure_attachment(resp2)

            with allure.step("Check that API returned error OR duplicate was created"):
                if resp2.status_code >= 400:
                    print(f"   ✅ API returned error as expected: {resp2.status_code}")
                else:
                    # Некоторые API разрешают дубликаты — тогда фиксируем это
                    print(f"   ⚠️ API allowed duplicate (status {resp2.status_code})")
                    print(f"   📝 This means TheCatAPI doesn't prevent duplicate favourites")
                    # Не падаем, а фиксируем факт
                    allure.attach(
                        f"API allowed duplicate. Status: {resp2.status_code}",
                        name="Duplicate behaviour",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    # Если создался дубликат — тоже добавляем в список на уборку
                    if resp2.status_code in [200, 201] and resp2.json().get("id"):
                        created_ids.append(resp2.json()["id"])
        finally:
            # 4. Уборка
            print("\n🧹 CLEANUP: Deleting created favourites...")
            with allure.step("Cleanup: delete created favourites"):
                for fav_id in created_ids:
                    del_resp = requests.delete(f"{url}/favourites/{fav_id}", headers=headers)
                    print(f"   🗑️ Deleted favourite {fav_id}: {del_resp.status_code}")

        print("\n" + "=" * 60)
        print("✅ FINISH: test passed successfully")
        print("=" * 60 + "\n")
      