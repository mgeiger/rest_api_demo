import sys

import jsonschema
import pytest
import requests


URL = "http://localhost:8888/api/blog/categories/"


get_schema = {
    "id": 0,
    "name": "string",
    "posts": [{
        "body": "string",
        "category": "string",
        "category_id": 0,
        "id": 0,
        "pub_date": "2020-06-14T16:18:24.586Z",
        "title": "string"
    }]
}


def available_ids():
    response = requests.get(URL)
    return [item['id'] for item in response.json()]
    

# Happy Path Testing
# TODO: Set this up with parametrize indirect/pytest_generate_tests
def test_get_blog_categories_id():
    """
    Ensures that each of the available IDs gets a response
    """
    for id in available_ids():
        response = requests.get(f"{URL}{id}")
        assert response.status_code == 200


@pytest.mark.depends(on=['test_get_blog_categories_id'])
def test_get_blog_categories_id_schema():
    """
    Ensures that each of the available IDs has the correct schema
    """
    for id in available_ids():
        response = requests.get(f"{URL}{id}")
        jsonschema.validate(response.json(), schema=get_schema)


# Negative
ids = [1, 2, 3]  # From Database
# TODO: Set this up with indirect/pytest_generate_tests
@pytest.mark.parametrize(
    'id', [max(ids)+1, 0, sys.maxsize, 'test']
)
def test_get_blog_categories_id_negative(id):
    url = f"{URL}{id}"
    response = requests.get(url)
    assert response.status_code == 404, f"URL {url} returned {response.status_code}, not 404"
