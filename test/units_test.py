from clientAPI.session import BaseFeature
from assertpy import assert_that
import pytest

@pytest.fixture(autouse=True)
def unit_api():
    return BaseFeature(url_path="units")
    
def test_add_unit(unit_api):
    response = unit_api.add_new(payload={
        "name": "gram",
        "description": "weight measurement"})
    data = response.json().get("data")
    assert_that(response.status_code).is_equal_to(201)
    assert_that(len(data)).is_not_empty

def test_get_unit_detail(unit_api):
    response = unit_api.get_detail(json={
        "unitId": unit_api.recovery.get_log("unitId")})
    data = response.json().get("data").get("units")
    assert_that(response.status_code).is_equal_to(200)
    assert_that(len(data)).is_greater_than_or_equal_to(2)

def test_get_unit_list(unit_api):
    response = unit_api.get_detail(json={
        "q": "gram",
        "page": "1"})
    units = response.json().get("data")["units"]
    assert_that(response.status_code).is_equal_to(200)
    assert_that(len(units)).is_greater_than_or_equal_to(1)

def test_update_unit(unit_api):
    unitId = unit_api.recovery.get_log("unitId")
    response = unit_api.update_data(query=unitId, payload={
        "name": "update-meter",
        "description": "no-meter"})
    data = response.json().get("data")
    assert_that(response.status_code).is_equal_to(200)
    assert_that(len(data)).is_not_empty

def test_delete_unit(unit_api):
    unitId = unit_api.recovery.get_log("unitId")
    response = unit_api.remove_data(query=unitId)
    data = response.json().get("data")
    assert_that(response.status_code).is_equal_to(200)
    assert_that(data).is_empty