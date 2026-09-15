import allure
import pytest
import requests

from config import url
from helpers.attach import allure_attachment
from checkers import check_status_200, check_status_401


@allure.suite("authentication")
class TestAuthentication:

    @allure.title("Endpoints without authentication return 401")
    @allure.description(
        "Проверяет, что методы во вкладке Basics: Favouring не работают без аутентификации."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.homework
    def test_endpoints_without_auth(self) -> None:
        """Требование 6: Без аутентификации методы во вкладке Basics: Favouring не работают."""
        print("\n" + "=" * 60)
        print("🚀 START: test_endpoints_without_auth")
        print("=" * 60)

        headers = {"Content-Type": "application/json"}  # БЕЗ x-api-key

        # ===== GET /favourites без ключа =====
        print("\n🔍 TEST 1: GET /favourites without auth")
        with allure.step("GET /favourites without API key"):
            resp_get = requests.get(f"{url}/favourites", headers=headers)
        print(f"   📡 Status: {resp_get.status_code}")
        print(f"   📥 Response: {resp_get.text}")
        allure_attachment(resp_get)
        check_status_401(resp_get)

        # ===== POST /favourites без ключа =====
        print("\n🔍 TEST 2: POST /favourites without auth")
        with allure.step("POST /favourites without API key"):
            resp_post = requests.post(
                f"{url}/favourites",
                headers=headers,
                json={"image_id": "test123", "sub_id": "no_auth_user"}
            )
        print(f"   📡 Status: {resp_post.status_code}")
        print(f"   📥 Response: {resp_post.text}")
        allure_attachment(resp_post)
        check_status_401(resp_post)

        print("\n" + "=" * 60)
        print("✅ FINISH: test passed successfully")
        print("=" * 60 + "\n")

    @allure.title("API key header is case-insensitive")
    @allure.description(
        "Проверяет, что при изменении регистра хедера x-api-key не возникает ошибки."
    )
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.homework
    def test_api_key_header_case_insensitive(self, headers: dict) -> None:
        """Требование 5: При изменении регистра хедера не возникает ошибки."""
        print("\n" + "=" * 60)
        print("🚀 START: test_api_key_header_case_insensitive")
        print("=" * 60)

        # Берём API-ключ из фикстуры
        api_key = headers["x-api-key"]

        # Разные варианты регистра хедера
        variants = [
            ("X-API-KEY", {"X-API-KEY": api_key, "Content-Type": "application/json"}),
            ("X-Api-Key", {"X-Api-Key": api_key, "Content-Type": "application/json"}),
            ("x-API-key", {"x-API-key": api_key, "Content-Type": "application/json"}),
        ]

        for header_name, variant_headers in variants:
            print(f"\n🔍 Testing header case: {header_name}")

            with allure.step(f"Send GET /favourites with header '{header_name}'"):
                resp = requests.get(f"{url}/favourites", headers=variant_headers)

            print(f"   📡 Status: {resp.status_code}")
            print(f"   📥 Response: {resp.text[:200]}")

            allure_attachment(resp)

            with allure.step(f"Check that status is NOT 401"):
                assert resp.status_code != 401, \
                    f"Header '{header_name}' not recognized: {resp.status_code}"
                print(f"   ✅ Header '{header_name}' works fine")

        print("\n" + "=" * 60)
        print("✅ FINISH: test passed successfully")
        print("=" * 60 + "\n")
       