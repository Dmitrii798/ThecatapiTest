import allure
import pytest
import requests

from config import url
from helpers.attach import allure_attachment
from checkers import (
    check_status_200,
    check_not_empty,
)
from schemas.favourite_schema import (
    check_favourite_schema,
    check_favourites_list_schema,
)


@allure.suite("favourites_crud")
class TestFavouritesCRUD:

    @allure.title("Add favourite and verify it appears in the system")
    @allure.description("Добавляет favourite и проверяет, что он появился в системе.")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.homework
    def test_add_favourite_and_verify(self, headers: dict) -> None:
        print("\n" + "=" * 60)
        print("🚀 START: test_add_favourite_and_verify")
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

        payload = {"image_id": image_id, "sub_id": "crud_test_user"}
        created_id = None

        try:
            # 2. Создаём favourite
            print("\n🔍 STEP 1: Creating favourite...")
            with allure.step("Create new favourite"):
                create_resp = requests.post(
                    f"{url}/favourites",
                    headers=headers,
                    json=payload
                )

            print(f"   📡 Status: {create_resp.status_code}")
            print(f"   📥 Response: {create_resp.text}")
            allure_attachment(create_resp)

            assert create_resp.status_code in [200, 201], \
                f"Failed to create favourite: {create_resp.text}"

            # ✅ ПРОВЕРКА СХЕМЫ ПРИ СОЗДАНИИ
            check_favourite_schema(create_resp)
            print(f"   ✅ Schema check passed")

            created_data = create_resp.json()
            created_id = created_data["id"]
            print(f"   ✅ Created favourite with id: {created_id}")

            # 3. Проверяем, что он появился в системе
            print("\n🔍 STEP 2: Verifying favourite appears in the list...")
            with allure.step("Get all favourites and verify new favourite exists"):
                list_resp = requests.get(f"{url}/favourites", headers=headers)

            print(f"   📡 Status: {list_resp.status_code}")
            allure_attachment(list_resp)
            check_status_200(list_resp)
            check_not_empty(list_resp)

            # ✅ ПРОВЕРКА СХЕМЫ СПИСКА
            check_favourites_list_schema(list_resp)
            print(f"   ✅ List schema check passed")

            all_favourites = list_resp.json()
            print(f"   📊 Total favourites: {len(all_favourites)}")

            found = any(fav["id"] == created_id for fav in all_favourites)
            assert found, f"Favourite with id {created_id} not found in the list"
            print(f"   ✅ Favourite {created_id} found in the list")

        finally:
            # 4. Уборка
            if created_id:
                print(f"\n🧹 CLEANUP: Deleting favourite {created_id}...")
                with allure.step(f"Cleanup: delete favourite {created_id}"):
                    del_resp = requests.delete(
                        f"{url}/favourites/{created_id}",
                        headers=headers
                    )
                    print(f"   🗑️ Delete status: {del_resp.status_code}")

        print("\n" + "=" * 60)
        print("✅ FINISH: test passed successfully")
        print("=" * 60 + "\n")
        