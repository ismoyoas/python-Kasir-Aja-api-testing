from clientAPI.session import AuthFeature
from assertpy import assert_that
import pytest

@pytest.fixture(scope="session")
def auth_api():
    return AuthFeature(store_name="Toko Serbaguna",
                       email="sample@ex.com",
                       password="123adsfadf@")

def test_user_registration(auth_api):
    response = auth_api.sign_up()
    data = response.json().get("data")
    assert_that(response.status_code).is_equal_to(201)
    assert_that(len(data)).is_greater_than_or_equal_to(1)

def test_user_login(auth_api):
    response = auth_api.sign_in()
    data = response.json().get('data')
    assert_that(response.status_code).is_equal_to(201)
    assert_that(len(data)).is_greater_than_or_equal_to(1)

def test_user_refresh_access(auth_api):
    response = auth_api.update_token()
    message = response.json().get('message')
    assert_that(response.status_code).is_equal_to(200)
    assert_that(message.lower()).contains('baru')

@pytest.mark.skip(reason="The test is skipped because it could interfere with the subsequent test.")
def test_user_logout(auth_api):
    response = auth_api.sign_out()
    message = response.json().get('message')
    assert_that(response.status_code).is_equal_to(200)
    assert_that(message.lower()).contains('hapus')