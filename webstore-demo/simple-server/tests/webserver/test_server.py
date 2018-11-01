import pytest
import json
from base64 import b64encode
from simpleserver.util.consts import ENTER, EXIT
from simpleserver.util.logger import SSLogger

myLogger = SSLogger(__name__).get_logger()

def test_get_info(client):
    myLogger.debug(ENTER)
    response = client.get('/info')
    json_data = json.loads(response.data)
    assert b"info" in response.data
    assert json_data.get('info') == 'index.html => Info in HTML format'
    myLogger.debug(EXIT)

def test_post_signin(client):
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

def test_post_login(client):
    myLogger.debug(ENTER)
    email = 'kari.karttinen@foo.com'
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'email': email,
        'password': 'Kari'
    }
    url = '/login'
    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.content_type == mimetype
    assert response.json['ret'] == 'ok'
    assert response.json['msg'] == 'Credentials ok'
    assert len(response.json['json-web-token']) > 20
    # Now try with wrong password.
    data = {
        'email': email,
        'password': 'WRONG-PASSWORD'
    }
    url = '/login'
    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.content_type == mimetype
    assert response.json['ret'] == 'failed'
    assert response.json['msg'] == 'Credentials are not good - either email or password is not correct'
    myLogger.debug(EXIT)

def get_token(client):
    myLogger.debug(ENTER)
    email = 'kari.karttinen@foo.com'
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'email': email,
        'password': 'Kari'
    }
    url = '/login'
    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.content_type == mimetype
    assert response.json['ret'] == 'ok'
    assert response.json['msg'] == 'Credentials ok'
    assert len(response.json['json-web-token']) > 20
    ret = response.json['json-web-token']
    return ret

def test_get_product_groups(client):
    myLogger.debug(ENTER)
    token = get_token(client)
    decoded_token = (b64encode(token.encode())).decode()
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Basic ' + decoded_token
    }
    url = '/product-groups'
    response = client.get(url, headers=headers)
    assert response.status == '200 OK'
    json_data = json.loads(response.data)
    assert json_data.get('ret') == 'ok'
    assert b"product-groups" in response.data
    product_groups = json_data.get('product-groups')
    assert product_groups['1'] == 'Books'
    assert product_groups['2'] == 'Movies'
    myLogger.debug(EXIT)

def test_get_products(client):
    myLogger.debug(ENTER)
    token = get_token(client)
    decoded_token = (b64encode(token.encode())).decode()
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Basic ' + decoded_token
    }
    url = '/products/1'
    response = client.get(url, headers=headers)
    assert response.status == '200 OK'
    json_data = json.loads(response.data)
    assert json_data.get('ret') == 'ok'
    assert b"product" in response.data
    products = json_data.get('products')
    assert len(products) == 35
    # Damn, coincidentally we got a great novel!
    assert products[30][2] == 'Simpauttaja'
    myLogger.debug(EXIT)

def test_get_product(client):
    myLogger.debug(ENTER)
    token = get_token(client)
    decoded_token = (b64encode(token.encode())).decode()
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Basic ' + decoded_token
    }
    url = '/product/2/49'
    response = client.get(url, headers=headers)
    assert response.status == '200 OK'
    json_data = json.loads(response.data)
    assert json_data.get('ret') == 'ok'
    assert b"product" in response.data
    product = json_data.get('product')
    assert len(product) == 8
    # What a coincidence! The chosen movie is the best western of all times!
    assert product[2] == 'Once Upon a Time in the West'
    myLogger.debug(EXIT)


