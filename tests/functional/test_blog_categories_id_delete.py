import copy
import logging
import random
import sys
import string

import pytest
import requests

URL = "http://localhost:8888/api/blog/categories/"

# The original DB has three categoires
# TODO: Fill out my own in a fixture and use that
IDS = [1, 2, 3]

# Base needed data for a post
BASE_DATA = {
    "title": "",
    "body": "",
    "category_id": 0
}

logger = logging.getLogger(__file__)


@pytest.mark.parametrize("id", IDS)
def test_delete_blog_categories_id(id):
    """
    Ensures that we can delete all of the categories by ID 
    in the original DB

    :param id: ID of the Category
    """
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
    """
    Ensure we get a 404 when trying to delete a category not there

    :param id: Test Category ID
    """
    url = f"{URL}{id}"
    response = requests.delete(url)
    assert response.status_code == 404


# @pytest.mark.skip(msg="Not Implemented")
def test_delete_blog_categories_id_in_use():
    """
    Ensure that we don't delete a category when in use
    """
    # Create a post with a category
    data = copy.deepcopy(BASE_DATA)

    # Get a Random Category
    response = requests.get("http://localhost:8888/api/blog/categories/")
    category = random.choice([i['id'] for i in response.json()])

    data['title'] = "".join([random.choice(string.ascii_letters) for _ in range(20)])
    data['body'] = "".join([random.choice(string.ascii_letters) for _ in range(20)])
    data['category_id'] = category

    response = requests.post(URL, json=data)
    assert response.status_code == 200

    # Attempt to delete the category while the post still exists
    url = f"{URL}{category}"
    response = requests.delete(url)
    assert response.status_code == 409
