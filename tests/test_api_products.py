import requests

from OpenCartDemoSimulation.utilities.configurations import getConfig, get_headers, send_get_request, getQuery
from OpenCartDemoSimulation.utilities.resources import ApiResources

def search_products(category_type):
    if category_type == "valid_id":
        category = "654854"
    elif category_type == "invalid_id":
        category = "56453"
    elif category_type == "non_numeric":
        category = "fghioj!@'"
    url = getConfig()['API']['endpoint'] + ApiResources.products_category + category
    headers = get_headers()
    response = send_get_request(url, headers)
    json_response = response.json()
    status_code = response.status_code
    return json_response,status_code

def test_valid_category_id():
    ## sends a get request to the API requesting all the products from category 24 so it can compare the name and price with the ones stored in the DB to see if API is bringing correct data
    json_response, _ = search_products("valid_id")
    products_in_response = [(product["id"],  product["name"],  product["price_excluding_tax_formated"])  for product in json_response["data"]]  # This loops through each dictionary in the "data" list, assigning it to the variable product one at a time. For each product dictionary, it extracts the value associated with the key "name" and price, creating a list with dictionary with all these names
    print(products_in_response)
    #[(28, 'HTC Touch HD', '$122.00'), (29, 'Palm Treo Pro', '$337.99'), (40, 'iPhone', '$123.20')]

    ###############
    # get the data from the same products in the DB
    query = "SELECT oc_product.product_id, oc_product_description.name, CONCAT('$',CONVERT(ROUND(oc_product.price, 2),CHAR))  FROM oc_product LEFT JOIN oc_product_description ON (oc_product.product_id = oc_product_description.product_id) LEFT JOIN oc_product_to_category ON (oc_product.product_id = oc_product_to_category.product_id) LEFT JOIN oc_category ON (oc_product_to_category.category_id = oc_category.category_id) WHERE oc_category.category_id = 24;"
    list_items = getQuery(query)
    print(list_items)
    #[(28, 'HTC Touch HD', '$100.00'), (29, 'Palm Treo Pro', '$279.99'), (40, 'iPhone', '$100.00')]

    assert set(products_in_response) == set(list_items), f"Expected {products_in_response} but got {list_items}"

def test_invalid_category_id():
    json_response, status_code = search_products("invalid_id")
    assert status_code == 200 and json_response["data"] == [], f"AssertionError: Expected status code 200 and empty product data. Received status code: {status_code} and product data: {json_response["data"]}"

def test_non_numeric_category_id():
    json_response, status_code = search_products("non_numeric")
    assert status_code == 200 and json_response[
        "data"] == [], f"AssertionError: Expected status code 200 and empty product data. Received status code: {status_code} and product data: {json_response["data"]}"

def test_missing_info_header():
    category = "24"
    url = getConfig()['API']['endpoint'] + ApiResources.products_category + category

    response = requests.get(url, headers={"X-Oc-Merchant-Id": "",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Connection": "keep-alive",
        "X-Oc-Session": "80f1194132d731c4bc97ecf8a2"})
    json_response = response.json()
    status_code = response.status_code
    assert status_code == 403 and json_response[
        "data"] == [], f"AssertionError: Expected status code 403 and empty product data. Received status code: {status_code} and product data: {json_response["data"]}"