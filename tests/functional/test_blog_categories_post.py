import time

import pytest
import requests


URL = "http://localhost:8888/api/blog/categories/"


def test_post_blog_categories():
    """
    Ensures that we can post a new Blog Category and return the correct status code
    """
    category_name = f"NEW CATEGORY {time.time()}"
    data = {
        "name": category_name
    }
    response = requests.post(url=URL, json=data)
    assert response.status_code == 201


def test_post_blog_categories_query():
    """
    Ensures that we can post a new Blog Category and it is found in the /categories API
    """
    category_name = f"NEW CATEGORY {time.time()}"
    data = {
        "name": category_name
    }
    response_post = requests.post(url=URL, json=data)

    # Verify that our information is there
    response_get = requests.get(url=URL)
    category_names = [item['name'] for item in response_get.json()]
    assert category_names in category_names, f"Category {category_name} not found in {category_names}"
