# helpers/attach.py
import allure


def allure_attachment(response) -> None:
    """Прикрепляет тело ответа к отчёту Allure."""
    with allure.step("Attach response to Allure report"):
        allure.attach(
            response.text,
            name="Response body",
            attachment_type=allure.attachment_type.JSON
        )
       