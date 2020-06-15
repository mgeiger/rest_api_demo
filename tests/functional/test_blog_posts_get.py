import logging

import pytest
import requests
from jsonschema import validate


URL = "http://localhost:8888/api/blog/posts/"

logger = logging.getLogger(__file__)


get_schema = {
    "page": 0,
    "pages": 0,
    "per_page": 0,
    "total": 0,
    "items": [{
        "body": "string",
        "category": "string",
        "category_id": 0,
        "id": 0,
        "pub_date": "2020-06-13T01:29:58.210Z",
        "title": "string"
    }]
}

# Happy Path Testing
def test_get_blog_posts_basic():
    """
    Ensures that we can retrieve blog posts information
    """
    response = requests.get(URL)
    assert response
    # Basic Response should be 200
    assert response.status_code == 200


@pytest.mark.depends(on=['test_get_blog_posts_basic'])
def test_get_blog_posts_schema():
    """
    Ensures the blog post matches the schema
    """
    response = requests.get(URL)
    validate(instance=response.json(), schema=get_schema)
