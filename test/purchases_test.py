from clientAPI.session import BaseFeature, SpecialFeature
from assertpy import assert_that
import pytest

@pytest.fixture(autouse=True)
def pchs_api():
    return BaseFeature(url_path="purchases")

@pytest.fixture(autouse=True)
def add_ons_api():
    return SpecialFeature(url_path='purchases')

def test_user_add_transaction(pchs_api):
    payload = {"officeId": pchs_api.recovery.get_log("user_data")["data"]["user"]["officeId"],
               "date": "2023-02-28",
               "invoice": "INV/02/12/2023/001",
               "amount": 14000,
               "discount": 0,
               "description": "testing",
               "items": [{
                   "productId": pchs_api.recovery.get_log("productId"),
                   "quantity": 4,
                   "cost": 1000}]}
    response = pchs_api.add_new(payload)
    data = response.json().get('data')
    assert_that(response.status_code).is_equal_to(201)
    assert_that(len(data)).is_not_empty

def test_user_get_transaction_detail(add_ons_api):
    purchaseId = add_ons_api.get_log("purchaseId")
    response = add_ons_api.get_detail(iD=purchaseId)
    data = response.json().get('data').get('purchase')
    assert_that(response.status_code).is_equal_to(200)
    assert_that(len(data)).is_not_empty

def test_user_get_transaction_list(pchs_api):
    response = pchs_api.get_detail(params={
        "startDate": "2023-01-29",
        "endDate": "2023-02-30"})
    purchases = response.json().get("data").get("purchases")
    assert_that(response.status_code).is_equal_to(200)
    assert_that(len(purchases)).is_greater_than_or_equal_to(1)