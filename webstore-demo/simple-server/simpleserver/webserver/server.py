from flask import Blueprint, render_template, jsonify, request
from simpleserver.util.consts import ENTER, EXIT
from simpleserver.util.logger import SSLogger
from simpleserver.domaindb.domain import Domain
from simpleserver.userdb.users import Users

bp = Blueprint('simpleserver', __name__)
myLogger = SSLogger(__name__).get_logger()
myDomain = Domain()
myUsers = Users()

def validate_parameters(myList):
    """ A very simple validator: just check that no item in the list is empty or None.
    myList - the list of parameters.
    Returns: true if parameters ok, false otherwise"""
    ret = not ((None in myList) or ('' in myList))
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
    """Posts the sign in.
    Validates parameters, then calls users module to add new user."""
    myLogger.debug(ENTER)
    first_name = request.get_json().get('first-name')
    last_name = request.get_json().get('last-name')
    email = request.get_json().get('email')
    password = request.get_json().get('password')
    validation_passed = validate_parameters([first_name, last_name, email, password])
    ret = myUsers.add_user(email, first_name, last_name, password) if validation_passed \
        else { 'ret': 'failed', 'msg': 'Validation failed - some fields were empty' }
    myLogger.debug(EXIT)
    return jsonify(ret)

