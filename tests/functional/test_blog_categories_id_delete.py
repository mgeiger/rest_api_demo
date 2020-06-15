import sys

import pytest
import requests

URL = "http://localhost:8888/api/blog/categories/"

IDS = [1, 2, 3]


@pytest.mark.parametrize("id", IDS)
def test_delete_blog_categories_id(id):
    url = f"{URL}{id}"
    response = requests.delete(url)
    assert response.status_code == 204

    # Ensure the ID is gone
    response = requests.get(url)
    assert response.status_code == 404
    # Ensure the ID is not in the list
    response = requests.get(URL)
    categories_ids = [item['id'] for item in response.json()]
    assert id not in categories_ids


@pytest.mark.parametrize('id', [max(IDS)+1, 0, sys.maxsize])
def test_delete_blog_categories_id_not_found(id):
    url = f"{URL}{id}"
    response = requests.delete(url)
    assert response.status_code == 404


@pytest.mark.skip(msg="Not Implemented")
def test_delete_blog_categories_id_in_use():
    """
    Ensure that we don't delete a category when in use
    """
    # Create a post with a category
    # Attempt to delete the category while the post still exists
    pass