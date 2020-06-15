
import requests
import pytest
import datetime

URL = 'http://localhost:8888/api/blog/posts/'


def test_get_blog_posts_archive_y():
    # Determine the post dates
    response = requests.get(URL)
    dates = [datetime.datetime.fromisoformat(item['pub_date']) for item in response.json()["items"]]
    years = [date.year for date in dates]
    # Cycle through all the post years
    for year in set(years):
        url = f"{URL}archive/{year}/"
        response = requests.get(url)
        assert response
        assert response.status_code == 200
        # TODO: Check Content Dates


def test_get_blog_posts_archive_ym():
    # Determine the post dates
    response = requests.get(URL)
    dates = [datetime.datetime.fromisoformat(item['pub_date']) for item in response.json()["items"]]
    ym = [(date.year, date.month) for date in dates]
    # Cycle through all the year/month
    for year_month in set(ym):
        url = f"{URL}archive/{year_month[0]}/{year_month[1]}/"
        response = requests.get(url)
        assert response
        assert response.status_code == 200
        # TODO: Check Content Dates


def test_get_blog_posts_archive_ymd():
    # Determine the post dates
    response = requests.get(URL)
    dates = [datetime.datetime.fromisoformat(item['pub_date']) for item in response.json()["items"]]
    ymd = [(date.year, date.month, date.day) for date in dates]
    # Cycle through all the year/month
    for year_month_day in set(ymd):
        url = f"{URL}archive/{year_month_day[0]}/{year_month_day[1]}/{year_month_day[2]}/"
        response = requests.get(url)
        assert response
        assert response.status_code == 200
        # TODO: Check Content Dates