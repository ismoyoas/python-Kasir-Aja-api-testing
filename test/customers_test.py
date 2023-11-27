from clientAPI.session import BaseFeature
from assertpy import assert_that
import pytest

@pytest.fixture(autouse=True)
def ctmr_api():
    return BaseFeature(url_path="customers")
    
def test_add_customer(ctmr_api):
    response = ctmr_api.add_new(payload={
        "name": "Budi",
        "phone": "081234567890",
        "address": "Bandoeng",
        "description": "Budi anak Pak Edi"})
    data = response.json().get("data")
    assert_that(response.status_code).is_equal_to(201)
    assert_that(len(data)).is_not_empty

def test_get_customer_detail(ctmr_api):
    response = ctmr_api.get_detail(json={
        "customerId": ctmr_api.recovery.get_log("customerId")})
    data = response.json().get("data").get("customers")
    assert_that(response.status_code).is_equal_to(200)
    assert_that(len(data)).is_greater_than_or_equal_to(2)

def test_get_customer_list(ctmr_api):
    response = ctmr_api.get_detail(json={
        "q": "Budi",
        "page": "1"})
    customers = response.json().get("data")["customers"]
    assert_that(response.status_code).is_equal_to(200)
    assert_that(len(customers)).is_greater_than_or_equal_to(1)

def test_update_customer(ctmr_api):
    ctmId = ctmr_api.recovery.get_log("customerId")
    response = ctmr_api.update_data(query=ctmId, payload={
        "name": "Budi Doremi",
        "phone": "08987654321",
        "address": "Bandung",
        "description": "Pelanggan VIP"})
    data = response.json().get("data")
    assert_that(response.status_code).is_equal_to(200)
    assert_that(len(data)).is_not_empty

def test_delete_customer(ctmr_api):
    ctmId = ctmr_api.recovery.get_log("customerId")
    response = ctmr_api.remove_data(query=ctmId)
    data = response.json().get("data")
    assert_that(response.status_code).is_equal_to(200)
    assert_that(data).is_empty