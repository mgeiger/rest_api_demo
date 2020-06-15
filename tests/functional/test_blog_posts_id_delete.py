import sys
import pytest
import requests

URL = "http://localhost:8888/api/blog/posts/"

IDS = [1, 2, 3, 4, 5]

# @pytest.mark.skip(msg="Not Implemented")
@pytest.mark.parametrize("id", IDS)
def test_delete_blog_posts_id(id):
    url = f"{URL}{id}"
    response = requests.delete(url)
    assert response.status_code == 204

    # Ensure the ID is gone
    response = requests.get(url)
    assert response.status_code == 404
    # Ensure the ID is not in the list
    response = requests.get(URL)
    posts_ids = [item['id'] for item in response.json()['items']]
    assert id not in posts_ids


@pytest.mark.parametrize('id', [max(IDS)+1, 0, sys.maxsize])
def test_delete_blog_posts_id_not_found(id):
    url = f"{URL}{id}"
    response = requests.delete(url)
    assert response.status_code == 404
