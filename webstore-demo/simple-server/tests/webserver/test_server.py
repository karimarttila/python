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

def test_info(client):
    myLogger.debug(ENTER)
    # NOTE: We cannot use 'jamppa.jamppanen@foo.com'
    # since test_users.py already adds it to user db.
    email = 'pena.jamppanen@foo.com'
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'first-name': 'Pena',
        'last-name': 'Jamppanen',
        'email': email,
        'password': 'JampanSalaSana'
    }
    url = '/signin'
    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.content_type == mimetype
    assert response.json['ret'] == 'ok'
    assert response.json['email'] == email
    # Try again, should fail now.
    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.content_type == mimetype
    assert response.json['ret'] == 'failed'
    assert response.json['email'] == email
    assert response.json['msg'] == 'Email already exists'
    myLogger.debug(EXIT)

