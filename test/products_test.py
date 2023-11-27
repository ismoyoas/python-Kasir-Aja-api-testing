from clientAPI.session import BaseFeature
from assertpy import assert_that
import pytest

@pytest.fixture(autouse=True)
def prd_api():
    return BaseFeature(url_path="products")
    
def test_add_product(prd_api):
    response = prd_api.add_new(payload={
        "category_id" : prd_api.recovery.get_log("categoryId"),
        "code": "A314ASDDFIER3432",
        "name": "taro",
        "price": 3500,
        "cost": 3000,
        "stock": 150})
    data = response.json().get("data")
    assert_that(response.status_code).is_equal_to(201)
    assert_that(len(data)).is_not_empty

def test_get_product_detail(prd_api):
    response = prd_api.get_detail(json={
        "productId": prd_api.recovery.get_log("productId")})
    data = response.json().get("data").get("products")
    assert_that(response.status_code).is_equal_to(200)
    assert_that(len(data)).is_not_empty

def test_get_product_list(prd_api):
    response = prd_api.get_detail(json={
        "page": 1,
        "q": "taro",
        "withStock": "true",
        "withCategory": "true",
        "categoryId": prd_api.recovery.get_log("categoryId")})
    products = response.json().get("data")["products"]
    assert_that(response.status_code).is_equal_to(200)
    assert_that(len(products)).is_greater_than_or_equal_to(1)

def test_update_product(prd_api):
    prdId = prd_api.recovery.get_log("productId")
    response = prd_api.update_data(query=prdId, payload={
        "category_id" : prd_api.recovery.get_log("categoryId"),
        "code": "A314ASDDFIER3432",
        "name": "taro",
        "price": "3500",
        "cost": "3000",
        "stock": "135"})
    data = response.json().get("data")
    assert_that(response.status_code).is_equal_to(200)
    assert_that(len(data)).is_not_empty

def test_delete_product(prd_api):
    prdId = prd_api.recovery.get_log("productId")
    response = prd_api.remove_data(query=prdId)
    data = response.json().get("data")
    assert_that(response.status_code).is_equal_to(200)
    assert_that(data).is_empty