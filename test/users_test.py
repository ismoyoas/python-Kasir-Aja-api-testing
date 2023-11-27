from clientAPI.session import BaseFeature
from assertpy import assert_that
import pytest

@pytest.fixture(scope="session")
def user_api():
    return BaseFeature(url_path="users")
    
def test_create_user(user_api):
    response = user_api.add_new(payload={
        "name": "kasir-serbaguna",
        "email": "user@example.com",
        "password": "jiasda2321@"})
    data = response.json().get("data")
    assert_that(response.status_code).is_equal_to(201)
    assert_that(len(data)).is_not_empty

def test_get_user_detail(user_api):
    response = user_api.get_detail(json={
        "userId": user_api.recovery.get_log("userId")})
    data = response.json().get("data").get("users")
    assert_that(response.status_code).is_equal_to(200)
    assert_that(len(data)).is_greater_than(1)

def test_get_user_list(user_api):
    response = user_api.get_detail(json={
        "q": "kasir-serbaguna",
        "p": "1"})
    users = response.json().get("data")["users"]
    assert_that(response.status_code).is_equal_to(200)
    assert_that(len(users)).is_greater_than_or_equal_to(1)

def test_update_user(user_api):
    userId = user_api.recovery.get_log("userId")
    response = user_api.update_data(query=userId, payload={
        "name": "update-user",
        "email": "user@example.com"})
    message = response.json().get("message")
    assert_that(response.status_code).is_equal_to(200)
    assert_that(message.lower()).contains("update")

def test_delete_user(user_api):
    userId = user_api.recovery.get_log("userId")
    response = user_api.remove_data(query=userId)
    message = response.json().get("message")
    assert_that(response.status_code).is_equal_to(200)
    assert_that(message.lower()).contains("hapus")