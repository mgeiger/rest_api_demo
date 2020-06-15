import random
import copy
import time
import pytest
import requests

URL = "http://localhost:8888/api/blog/posts/"

IDS = [1, 2, 3, 4, 5]  # Should be a query to the system to get the Posts IDs
UPDATES = ['title', 'body', 'category_id']


@pytest.mark.parametrize('id', IDS)
@pytest.mark.parametrize('field', UPDATES)
def test_put_blog_posts_id(id, field):
    url = f"{URL}{id}"
    # Get the original field value
    original_response = requests.get(url)
    assert original_response.status_code == 200, f"Original value did not return 200, returned {original_response.status_code}: {original_response.text}"
    original_value = original_response.json()[field]
    # Update Original with new data
    if field == 'category_id':
        # Pick a random new category
        response = requests.get("http://localhost:8888/api/blog/categories/")
        category_ids = set([item['id'] for item in response.json()])
        category_ids.remove(original_value)
        new_value = random.choice(list(category_ids))
    else:
        # Add a random number to the front of the string
        new_value = f"{random.randrange(10)}{original_value}"

    # Use PUT to update
    data = copy.deepcopy(original_response.json())
    data[field] = new_value
    requests.put(url, json=data)
    # Readback to ensure it wrote correctly
    response = requests.get(url)
    updated_value = response.json()[field]
    assert updated_value == new_value
    assert updated_value != original_value


@pytest.mark.skip(msg="Not Implemented")
def test_put_blog_posts_id_max_values():
    pass