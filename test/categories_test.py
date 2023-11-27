from clientAPI.session import BaseFeature
from assertpy import assert_that
import pytest

@pytest.fixture(autouse=True)
def catg_api():
    return BaseFeature(url_path="categories")
    
def test_add_category(catg_api):
    response = catg_api.add_new(logger="categoryId",payload={
        "name": "makanan ringan",
        "description": "makanan ringan dari indofood"})
    data = response.json().get("data")
    assert_that(response.status_code).is_equal_to(201)
    assert_that(len(data)).is_not_empty

def test_get_category_detail(catg_api):
    response = catg_api.get_detail(json={
        "categoryId": catg_api.recovery.get_log("categoryId")})
    data = response.json().get("data").get("categories")
    assert_that(response.status_code).is_equal_to(200)
    assert_that(len(data)).is_greater_than_or_equal_to(2)

def test_get_category_list(catg_api):
    response = catg_api.get_detail(json={
        "q": "makanan",
        "page": "1"})
    categories = response.json().get("data")["categories"]
    assert_that(response.status_code).is_equal_to(200)
    assert_that(len(categories)).is_not_empty

def test_update_category(catg_api):
    catgId = catg_api.recovery.get_log("categoryId")
    response = catg_api.update_data(query=catgId, payload={
        "name": "update-minuman",
        "description": "no-minuman"})
    data = response.json().get("data")
    assert_that(response.status_code).is_equal_to(200)
    assert_that(len(data)).is_not_empty

def test_delete_category(catg_api):
    catgId = catg_api.recovery.get_log("categoryId")
    response = catg_api.remove_data(query=catgId)
    data = response.json().get("data")
    assert_that(response.status_code).is_equal_to(200)
    assert_that(data).is_empty