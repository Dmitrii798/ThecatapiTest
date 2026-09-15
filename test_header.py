import allure
import pytest
import requests

from config import url
from helpers.attach import allure_attachment
from checkers import check_status_200


@allure.suite("headers")
class TestHeaders:

    @allure.title("Wrong Content-Type on POST /favourites returns error")
    @allure.description(
        "Проверяет, что при неправильном Content-Type при добавлении favourite "
        "возникает ошибка."
    )
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.homework
    def test_add_favourite_wrong_content_type(self, headers: dict) -> None:
        """Требование 4: Если поменять content-type при добавлении favourite, то возникает ошибка."""
        print("\n" + "=" * 60)
        print("🚀 START: test_add_favourite_wrong_content_type")
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

        # 2. Отправляем POST с неправильным Content-Type
        wrong_headers = headers.copy()
        wrong_headers["Content-Type"] = "text/plain"

        # Отправляем как "сырой" текст, а не JSON
        payload = f'{{"image_id": "{image_id}", "sub_id": "wrong_content_test"}}'

        print("\n🔍 MAIN TEST: Sending POST with Content-Type: text/plain")
        print(f"   📤 Payload (raw string): {payload}")

        with allure.step("Send POST with Content-Type: text/plain"):
            resp = requests.post(
                f"{url}/favourites",
                headers=wrong_headers,
                data=payload  # используем data, а не json
            )

        print(f"   📡 Status: {resp.status_code}")
        print(f"   📥 Response: {resp.text}")

        allure_attachment(resp)

        with allure.step("Check that API returned an error"):
            assert resp.status_code >= 400, \
                f"Expected error for wrong Content-Type, got {resp.status_code}"
            print(f"   ✅ Error received as expected")

        print("\n" + "=" * 60)
        print("✅ FINISH: test passed successfully")
        print("=" * 60 + "\n")

    @allure.title("Downloaded image is a valid JPEG")
    @allure.description(
        "Скачивает картинку кота и проверяет, что файл — валидный JPEG."
    )
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.homework
    def test_download_image_is_valid_jpeg(self, headers: dict) -> None:
        """Требование 9: Скачайте одну из картинок и убедитесь, что скачанный файл – это валидный jpeg."""
        print("\n" + "=" * 60)
        print("🚀 START: test_download_image_is_valid_jpeg")
        print("=" * 60)

        # 1. Получаем URL картинки через API
        print("\n📦 PRECONDITION: Getting a random image URL...")
        with allure.step("Get a random image URL from /images/search"):
            search_resp = requests.get(
                f"{url}/images/search",
                params={"limit": 1},
                headers=headers
            )
        check_status_200(search_resp)
        image_data = search_resp.json()[0]
        image_url = image_data["url"]
        image_id = image_data["id"]
        print(f"   🐱 image_id: {image_id}")
        print(f"   🔗 URL: {image_url}")

        # 2. Скачиваем картинку
        print("\n🔍 MAIN TEST: Downloading image...")
        with allure.step(f"Download image from {image_url}"):
            img_resp = requests.get(image_url)

        print(f"   📡 Status: {img_resp.status_code}")
        print(f"   📦 Content-Type: {img_resp.headers.get('Content-Type')}")
        print(f"   📏 Size: {len(img_resp.content)} bytes")
        print(f"   🔢 First 3 bytes (hex): {img_resp.content[:3].hex()}")

        allure_attachment(img_resp)
        assert img_resp.status_code == 200, \
            f"Failed to download image: {img_resp.status_code}"

        # 3. Проверяем Content-Type
        with allure.step("Check Content-Type is image/jpeg"):
            content_type = img_resp.headers.get("Content-Type", "")
            assert "image/jpeg" in content_type, \
                f"Expected image/jpeg, got {content_type}"
            print(f"   ✅ Content-Type is correct")

        # 4. Проверяем сигнатуру JPEG (магические байты)
        # JPEG-файлы начинаются с FF D8 FF
        with allure.step("Check JPEG signature (magic bytes FF D8 FF)"):
            first_bytes = img_resp.content[:3]
            assert first_bytes == b'\xff\xd8\xff', \
                f"Not a valid JPEG. First bytes: {first_bytes.hex()}"
            print(f"   ✅ JPEG signature is correct")

        # 5. Проверяем конец JPEG (должен заканчиваться на FF D9)
        with allure.step("Check JPEG end marker (FF D9)"):
            last_bytes = img_resp.content[-2:]
            assert last_bytes == b'\xff\xd9', \
                f"Invalid JPEG end. Last bytes: {last_bytes.hex()}"
            print(f"   ✅ JPEG end marker is correct")

        # 6. Прикрепляем картинку к отчёту Allure
        with allure.step("Attach image to Allure report"):
            allure.attach(
                img_resp.content,
                name=f"Downloaded Cat ({image_id})",
                attachment_type=allure.attachment_type.JPG
            )
            print(f"   📎 Image attached to Allure report")

        print("\n" + "=" * 60)
        print("✅ FINISH: test passed successfully")
        print("=" * 60 + "\n")
       