import pytest
from django.test import Client


@pytest.mark.smoke
def test_api():
    response = Client().get("/admin/")
    assert 200 <= response.status_code < 400
