
import logging
import os
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

import psutil
import pytest

HTTP_PORT = 8888

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s  %(filename)s  %(levelname)s] %(message)s'
)
logger = logging.getLogger(__file__)


@pytest.fixture(scope='session', autouse=True)
def backed_up_database():
    """
    Attempts to preserve the database given with this sample code.
    We want the database consistent per test execution for reproduciton purposes.
    Restores database at the conclusion of the test
    """
    original_name = "db.sqlite"
    backup_name = "db.sqlite.bak"
    p_orig = Path(__file__).parents[2] / f'rest_api_demo/{original_name}'
    p_back = Path(__file__).parents[2] / f'rest_api_demo/{backup_name}'
    logger.debug(f"Backing up Database {original_name} to {backup_name}")
    shutil.copy(p_orig, p_back)

    yield

    # Copy backup to original
    logger.debug(f"Restoring Database {backup_name} to {original_name}")
    shutil.copy(p_back, p_orig)
    p_back.unlink()


@pytest.fixture(scope='session', autouse=True)
@pytest.mark.usefixtures('backed_up_database')
def running_server(backed_up_database):
    """
    Start up the Flask rest_api_demo server

    :param backed_up_database: Pytest Fixture to ensure we backup the DB first
    """
    # This should be in a configuration somewhere
    p = Path(__file__).parents[2] / 'rest_api_demo/app.py'
    logger.debug("Starting Flask Server")
    process = subprocess.Popen(
        [sys.executable, str(p)], 
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    # TODO: What happens when the server is already running
    time.sleep(5)  # Startup Server
    
    # Ensure HTTP port is open
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        assert not s.connect_ex(('localhost', HTTP_PORT))
    finally:
        if s:
            s.close()
    
    yield

    logger.debug("Terminating Flask Server")
    # Ensure the port is closed
    p = psutil.Process(process.pid)
    p.terminate()
    time.sleep(5)  # Shut down server

    # Ensure HTTP port is open
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        assert s.connect_ex(('localhost', HTTP_PORT))
    finally:
        if s:
            s.close()
