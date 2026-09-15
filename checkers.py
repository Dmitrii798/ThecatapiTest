# checkers.py
import allure
import datetime


def check_status_200(response) -> None:
    with allure.step("Check status code 200"):
        assert response.status_code == 200, f"Bad request: {response.status_code}"


def check_not_empty(response) -> None:
    with allure.step("Check that response is not empty"):
        json_data = response.json()
        assert json_data is not None, "Empty response"
        assert len(json_data) > 0, "Empty response"


def check_response_length(response, len_my: int) -> None:
    with allure.step(f"Check the length of the response (expected <= {len_my})"):
        json_data = response.json()
        assert len(json_data) <= len_my, f"Wrong length: {len(json_data)} > {len_my}"


def check_dates_order_desc(response) -> None:
    with allure.step("Check dates order DESC (newest first)"):
        json_data = response.json()
        dates = [item.get("created_at") for item in json_data if item.get("created_at")]
        assert len(dates) > 0, "No created_at dates found"

        parsed_dates = []
        for date_str in dates:
            clean_date = date_str.replace("Z", "+00:00")
            dt = datetime.datetime.fromisoformat(clean_date)
            parsed_dates.append(dt)

        for i in range(len(parsed_dates) - 1):
            assert parsed_dates[i] >= parsed_dates[i + 1], (
                f"Dates not in DESC order: "
                f"{parsed_dates[i]} < {parsed_dates[i + 1]}"
            )

        allure.attach(
            "\n".join([str(d) for d in parsed_dates]),
            name="Parsed dates (DESC)",
            attachment_type=allure.attachment_type.TEXT
        )


def check_empty_response(response) -> None:
    """Проверка, что ответ — пустой список."""
    with allure.step("Check that response is empty list"):
        json_data = response.json()
        assert json_data is not None, "Response is None"
        assert isinstance(json_data, list), f"Response is not a list: {type(json_data)}"
        assert len(json_data) == 0, f"Expected empty list, got {len(json_data)} items"


def check_status_401(response) -> None:
    """Проверка статус-кода 401 (Unauthorized)."""
    with allure.step("Check status code 401"):
        assert response.status_code == 401, \
            f"Expected 401, got {response.status_code}: {response.text}"
        