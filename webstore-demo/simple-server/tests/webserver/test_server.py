import pytest
import json
from simpleserver.util.consts import ENTER, EXIT
from simpleserver.util.logger import SSLogger

myLogger = SSLogger(__name__).get_logger()

def test_info(client):
    myLogger.debug(ENTER)
    response = client.get('/info')
    json_data = json.loads(response.data)
    assert b"info" in response.data
    assert json_data.get('info') == 'index.html => Info in HTML format'
    myLogger.debug(EXIT)

