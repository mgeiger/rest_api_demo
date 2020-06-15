import logging

import jsonschema
import pytest
import requests


URL = "http://localhost:8888/api/blog/categories/"

logger = logging.getLogger(__file__)

get_schema = [{
    "id": 0,
    "name": "string"
}]


# Happy Path Testing
def test_get_blog_categories_basic():
    """
    Ensures that we can retrieve data about categories
    """
    response = requests.get(URL)
    assert response
    # Basic Response should be 200
    assert response.status_code == 200


@pytest.mark.xfail(reason="FIXME: Schema Validation Not Working on GET")
@pytest.mark.depends(on=['test_get_blog_categories_basic'])
def test_get_blog_categories_schema():
    """
    Ensures the schema matches properly
    """
    response = requests.get(URL)
    jsonschema.validate(instance=response.json(), schema=get_schema)


@pytest.mark.depends(on=['test_get_blog_categories_basic'])
def test_get_blog_categories_list():
    """
    Ensures that we return a list from the query
    """
    response = requests.get(URL)
    assert isinstance(response.json(), list)
