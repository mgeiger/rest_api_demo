import copy
import random
import string

import pytest
import requests

URL = "http://localhost:8888/api/blog/posts/"

# Add a New Blog Post after the first
# Need title, body, category_id
# Overwriting a id already existing
# Checking timestamp matches

BASE_DATA = {
    "title": "",
    "body": "",
    "category_id": 0
}


def test_post_blog_posts_status():
    """
    Ensures that we create a blog post using the POST
    """
    data = copy.deepcopy(BASE_DATA)

    # Get a Random Category
    response = requests.get("http://localhost:8888/api/blog/categories/")
    category = random.choice([i['id'] for i in response.json()])

    data['title'] = "".join([random.choice(string.ascii_letters) for _ in range(20)])
    data['body'] = "".join([random.choice(string.ascii_letters) for _ in range(20)])
    data['category_id'] = category

    response = requests.post(URL, json=data)
    assert response.status_code == 200  # The swagger doc says 200? 201 is created


def test_post_blog_posts_response():
    """
    Ensures our DB is updated with the newly posted Blog post
    """
    data = copy.deepcopy(BASE_DATA)

    # Get a Random Category
    response = requests.get("http://localhost:8888/api/blog/categories/")
    category = random.choice([i['id'] for i in response.json()])

    data['title'] = "".join([random.choice(string.ascii_letters) for _ in range(20)])
    data['body'] = "".join([random.choice(string.ascii_letters) for _ in range(20)])
    data['category_id'] = category

    response = requests.post(URL, json=data)
    assert response

    # Ensure it posted
    response = requests.get(URL)
    bodies = [item['body'] for item in response.json()['items']]
    titles = [item['title'] for item in response.json()['items']]
    assert (data['title'] in titles) and (data['body'] in bodies)



def test_post_blog_posts_unknown_category():
    data = copy.deepcopy(BASE_DATA)

    # Ensure our category is not there
    response = requests.get("http://localhost:8888/api/blog/categories/")
    current_category_ids = [i['id'] for i in response.json()]

    bad_category_id = max(current_category_ids) + 100
    data['title'] = "".join([random.choice(string.ascii_letters) for _ in range(20)])
    data['body'] = "".join([random.choice(string.ascii_letters) for _ in range(20)])
    data['category_id'] = bad_category_id

    response = requests.post(URL, json=data)
    assert response.status_code == 404
