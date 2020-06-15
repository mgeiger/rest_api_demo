import sys

import jsonschema
import requests
import pytest


URL = "http://localhost:8888/api/blog/posts/"

get_schema = {
    "body": "string",
    "category": "string",
    "category_id": 0,
    "id": 0,
    "pub_date": "2020-06-14T16:18:24.631Z",
    "title": "string"
}


def available_ids():
    response = requests.get(URL)
    return [item['id'] for item in response.json()['items']]


ids = [1,2,3,4,5]

# Happy Path
# TODO: Set this up with indirect/pytest_generate_tests
@pytest.mark.parametrize("id", ids)
def test_get_blog_posts_id_basic(id):
    url = f"{URL}{id}"
    response = requests.get(url)
    assert response.status_code == 200, f"URL {url} returned {response.status_code}, not 200"


@pytest.mark.parametrize("id", ids)
def test_get_blog_posts_id_schema(id):
    url = f"{URL}{id}"
    response = requests.get(url)
    jsonschema.validate(response.json(), get_schema)


# Negative Path
@pytest.mark.parametrize(
    'id', [max(ids)+1, 0, sys.maxsize, 'test']
)
def test_get_blog_posts_id_negative(id):
    url = f"{URL}{id}"
    response = requests.get(url)
    assert response.status_code == 404, f"URL {url} returned {response.status_code}, not 404"
