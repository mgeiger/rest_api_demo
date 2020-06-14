# Blog Tests

## Overview

[PyTest](https://docs.pytest.org/en/stable/) was chosen as the simple testing framework for this web application.

This framework was chosen for the following reasons:

* Extensible use of fixtures, both setup and teardown
* Communitity developed Plugin Functionality and expansion
* Simple & small assertions within tests
* The originator's familiariy with the framework


## Execution of Tests

### Functional Tests

#### Theory of Functional Testing

The goal here was to leave as much of the original application alone while exercising each of the REST API endpoints.

We want to start with a clean and repeatable setup prior to conducting any tests and leave the state as it was found.

*Testing has only been conducted on a Linux setup*

As part of fixturing, the functional tests will automatically start the flask server (`rest_api_demo/app.py`) and make a backup of the database flat file (`db.sqlite`).
The teardown of the fixtures will stop the server and restore the database.

#### Actual Execution of Functional Testing

1. Setup your Envrionment

This is the basic behind this process main repository:

**N.B.: Linux Only for now**

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python setup.py develop
python -m pip install -r requirements-test.txt
```

**You do not need to start the flask server, as the test infrastructure will take care of that.**

This will enable your virtual environment and install the necesary packages for testing.

2. Execution The Tests

As long as you follow the steps above, you should be ready to conduct the tests.
If you are not in your virtual environment, please re-source it with `source venv/bin/activate` (Linux).

The tests can be run simply from the command line using the following command set:

```bash
python -m pytest --verbose \
    --html="functional.html" \
    --junitxml="functional.xml" \
    tests/functional
```

This will run all of the tests in the `tests/functional` directory. 
The output may look something similar to this:

```
(venv) user@host:~$ pytest --verbose tests/functional/
=========== test session starts ============
platform linux -- Python 3.8.2, pytest-5.4.3, py-1.8.1, pluggy-0.13.1 -- /home/user/rest_api_demo/venv/bin/python3.8
cachedir: .pytest_cache
metadata: {'Python': '3.8.2', 'Platform': 'Linux-5.4.0-33-generic-x86_64-with-glibc2.29', 'Packages': {'pytest': '5.4.3', 'py': '1.8.1', 'pluggy': '0.13.1'}, 'Plugins': {'metadata': '1.9.0', 'html': '2.1.1'}}
rootdir: /home/rest_api_demo/tests, inifile: pytest.ini
plugins: metadata-1.9.0, html-2.1.1
collected 11 items                              

tests/functional/test_blog_categories.py::test_get_blog_categories PASSED [  9%]
tests/functional/test_blog_categories.py::test_post_blog_categories PASSED [ 18%]
tests/functional/test_blog_categories.py::test_delete_blog_categories_id PASSED [ 27%]
tests/functional/test_blog_categories.py::test_get_blog_categories_id PASSED [ 36%]
tests/functional/test_blog_categories.py::test_put_blog_categoires_id PASSED [ 45%]
tests/functional/test_blog_posts.py::test_get_blog_posts PASSED [ 54%]
tests/functional/test_blog_posts.py::test_post_blog_posts PASSED [ 63%]
tests/functional/test_blog_posts.py::test_get_blog_posts_archive PASSED [ 72%]
tests/functional/test_blog_posts.py::test_delete_blog_posts_id PASSED [ 81%]
tests/functional/test_blog_posts.py::test_get_blog_posts_id PASSED [ 90%]
tests/functional/test_blog_posts.py::test_put_blog_posts_id PASSED [100%]

=========== 11 passed in 10.06s ============
(venv) user@host:~rest_api_demo$ 
```

This command also includes two output files: `functional.xml` and `functional.html`.

The `functional.xml` is a Junit style output file that can be used as an input to CI based systems for test trends and analysis.
This feature is part of the core the [`pytest`](https://docs.pytest.org/en/stable/usage.html#creating-junitxml-format-files).

The `functional.html` file is for human-readable analysis of the test results. 
This is output from the [pytest-html](https://github.com/pytest-dev/pytest-html) plugin added in the `requirements-test.txt` file.

The runs can also be modified to run only a single file by changing the following in your execution:

`tests/functional/` to `tests/functional/test_blog_categories.py`

You may also run a single test case with the following:
`tests/functional/test_blog_categories.py::test_get_blog_categories`

### Integration Tests

TBD

### Unit Tests

TBD