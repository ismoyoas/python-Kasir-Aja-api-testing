from clientAPI.session import SpecialFeature, BaseFeature
from assertpy import assert_that
import pytest

@pytest.fixture(autouse=True)
def sales_api():
    return BaseFeature(url_path='sales')

@pytest.fixture(autouse=True)
def add_ons_api():
    return SpecialFeature(url_path='sales')
    
def test_user_add_sales(sales_api: BaseFeature):
    payload = {"officeId": sales_api.recovery.get_log("user_data")["data"]["user"]["officeId"],
               "customerId": sales_api.recovery.get_log("customerId"),
               "date": "2023-02-01",
                 "invoice": "INV001",
                 "amount": 2000,
                 "discount": 0,
                 "description": "Pembelian pertama",
                 "items" : [
                     {"productId": sales_api.recovery.get_log("productId"),
                      "quantity": 50,
                      "price": 2000}]
                      }
    response = sales_api.add_new(payload)
    data = response.json().get('data')
    assert_that(response.status_code).is_equal_to(201)
    assert_that(len(data)).is_not_empty

def test_user_get_sales_detail(add_ons_api):
    saleId = add_ons_api.get_log("saleId")
    response = add_ons_api.get_detail(iD=saleId)
    data = response.json().get('data').get('sale')
    assert_that(response.status_code).is_equal_to(200)
    assert_that(len(data)).is_not_empty

def test_user_get_sales_list(sales_api):
    response = sales_api.get_detail(params={
        "startDate": "2023-01-29",
        "endDate": "2023-02-30"})
    sales = response.json().get("data").get("sales")
    assert_that(response.status_code).is_equal_to(200)
    assert_that(len(sales)).is_greater_than_or_equal_to(1)