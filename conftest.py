# conftest.py
import os
import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def headers() -> dict:
    api_key = os.getenv("THE_CAT_API_KEY")
    if not api_key:
        pytest.fail("API key not found in .env")
    return {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
