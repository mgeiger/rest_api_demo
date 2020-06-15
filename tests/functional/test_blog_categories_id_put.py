import time

import pytest
import requests

URL = "http://localhost:8888/api/blog/categories/"


ids = [1, 2, 3]

# Happy Path
@pytest.mark.parametrize('id', ids)
def test_blog_categories_id_put_success(id):
    url = f"{URL}{id}"
    response = requests.get(url)
    original_name = response.json()['name']
    # Setup a new name
    new_name = f"{original_name} {time.time()}"
    data = {
        "name": new_name
    }
    response = requests.put(url, json=data)
    assert response.status_code == 204
    # Verify it was updated
    response = requests.get(url)
    assert response.json()['name'] == new_name


# Negative Path
@pytest.mark.parametrize('id', [max(ids)+1, 0])
def test_blog_categories_id_put_not_found(id):
    url = f"{URL}{id}"
    new_name = "Fake Name"
    data = {
        "name": new_name
    }
    response = requests.put(url, json=data)
    assert response.status_code == 404