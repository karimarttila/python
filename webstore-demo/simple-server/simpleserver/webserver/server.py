from base64 import b64decode
from http import HTTPStatus

from flask import Blueprint, render_template, jsonify, request

from simpleserver.domaindb.domain import Domain
from simpleserver.userdb.users import Users
from simpleserver.util.consts import ENTER, EXIT
from simpleserver.util.logger import SSLogger
from simpleserver.webserver.session import Session

bp = Blueprint('simpleserver', __name__)
myLogger = SSLogger(__name__).get_logger()
myDomain = Domain()
myUsers = Users()
mySession = Session()


def validate_parameters(my_list):
    """ A very simple validator: just check that no item in the list is empty or None.
    myList - the list of parameters.
    Returns: true if parameters ok, false otherwise"""
    myLogger.debug(ENTER)
    ret = not ((None in my_list) or ('' in my_list))
    myLogger.debug(EXIT)
    return ret


def is_valid_token(auth):
    """Validates the Json web token in authorization header parameter.
    auth - authorization header parameter
    returns {object} object {:email :exp} if success, None otherwise"""
    myLogger.debug(ENTER)
    ret = None
    if (auth is None) or (len(auth) == 0):
        myLogger.warning('Authorization not found in the header parameters')
    else:
        auth_rest = auth[6:]  # Get rid of 'Basic '
        decoded = (b64decode(auth_rest)).decode()
        index = decoded.find(':NOT')
        if index == -1:
            token = decoded
        else:
            token = decoded[0:index]
        myLogger.debug('token: ' + token)
        ret = mySession.validate_json_web_token(token)
    myLogger.debug(EXIT)
    return ret


# noinspection PyUnresolvedReferences
@bp.route('/index.html')
def get_index_page():
    """Gets index.html."""
    myLogger.debug(ENTER)
    myLogger.debug(EXIT)
    return render_template('index.html')


@bp.route('/info', methods=(['GET']))
def get_info():
    """Gets the info."""
    myLogger.debug(ENTER)
    ret = {'info': 'index.html => Info in HTML format'}
    myLogger.debug(EXIT)
    return jsonify(ret)


@bp.route('/signin', methods=(['POST']))
def post_signin():
    """Processes the sign in post.
    Validates parameters, then calls users module to add new user."""
    myLogger.debug(ENTER)
    first_name = request.get_json().get('first-name')
    last_name = request.get_json().get('last-name')
    email = request.get_json().get('email')
    password = request.get_json().get('password')
    validation_passed = validate_parameters([first_name, last_name, email, password])
    ret = myUsers.add_user(email, first_name, last_name, password) if validation_passed \
        else {'ret': 'failed', 'msg': 'Validation failed - some fields were empty'}
    http_status_code = HTTPStatus.OK if ret['ret'] == 'ok' else HTTPStatus.BAD_REQUEST
    myLogger.debug(EXIT)
    return jsonify(ret), http_status_code


@bp.route('/login', methods=(['POST']))
def post_login():
    """Processes the login post.
    Validates parameters, then calls users module to login."""
    myLogger.debug(ENTER)
    email = request.get_json().get('email')
    password = request.get_json().get('password')
    validation_passed = validate_parameters([email, password])
    if validation_passed:
        credentials_ok = myUsers.check_credentials(email, password)
        if credentials_ok:
            json_web_token = mySession.create_json_web_token(email)
            if json_web_token is not None:
                ret = {'ret': 'ok', 'msg': 'Credentials ok', 'json-web-token': json_web_token}
            else:
                myLogger.error('Could not create token')
                ret = {'ret': 'failed', 'msg': 'Could not create token'}
        else:
            ret = {'ret': 'failed', 'msg': 'Credentials are not good - either email or password is not correct'}
    else:
        ret = {'ret': 'failed', 'msg': 'Validation failed - some fields were empty'}
    http_status_code = HTTPStatus.OK if ret['ret'] == 'ok' else HTTPStatus.BAD_REQUEST
    myLogger.debug(EXIT)
    return jsonify(ret), http_status_code


@bp.route('/product-groups', methods=(['GET']))
def get_product_groups():
    """Processes the product-groups get request.
    Validates parameters, then calls domain module to get the requested entities."""
    myLogger.debug(ENTER)
    auth = request.headers['Authorization']
    token = is_valid_token(auth)
    if token is None:
        ret = {'ret': 'failed', 'msg': 'Given token is not valid'}
    else:
        my_product_groups = myDomain.get_product_groups()
        ret = {'ret': 'ok', 'product-groups': my_product_groups}
    http_status_code = HTTPStatus.OK if ret['ret'] == 'ok' else HTTPStatus.BAD_REQUEST
    myLogger.debug(EXIT)
    return jsonify(ret), http_status_code


@bp.route('/products/<int:pg_id>', methods=(['GET']))
def get_products(pg_id):
    """Processes the products get request.
    Validates parameters, then calls domain module to get the requested entities."""
    myLogger.debug(ENTER)
    auth = request.headers['Authorization']
    token = is_valid_token(auth)
    if token is None:
        ret = {'ret': 'failed', 'msg': 'Given token is not valid'}
    else:
        my_products = myDomain.get_products(pg_id)
        ret = {'ret': 'ok', 'products': my_products}
    http_status_code = HTTPStatus.OK if ret['ret'] == 'ok' else HTTPStatus.BAD_REQUEST
    myLogger.debug(EXIT)
    return jsonify(ret), http_status_code


@bp.route('/product/<int:pg_id>/<int:p_id>', methods=(['GET']))
def get_product(pg_id, p_id):
    """Processes the product get request.
    Validates parameters, then calls domain module to get the requested entities."""
    myLogger.debug(ENTER)
    auth = request.headers['Authorization']
    token = is_valid_token(auth)
    if token is None:
        ret = {'ret': 'failed', 'msg': 'Given token is not valid'}
    else:
        my_product = myDomain.get_product(pg_id, p_id)
        ret = {'ret': 'ok', 'product': my_product}
    http_status_code = HTTPStatus.OK if ret['ret'] == 'ok' else HTTPStatus.BAD_REQUEST
    myLogger.debug(EXIT)
    return jsonify(ret), http_status_code

