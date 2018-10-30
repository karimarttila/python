from flask import Blueprint, render_template, jsonify

from simpleserver.util.consts import ENTER, EXIT
from simpleserver.util.logger import SSLogger

bp = Blueprint('simpleserver', __name__)

myLogger = SSLogger(__name__).get_logger()

# noinspection PyUnresolvedReferences
@bp.route('/')
def index():
    """Show index.html."""
    myLogger.debug(ENTER)
    myLogger.debug(EXIT)
    return render_template('index.html')


@bp.route('/info', methods=(['GET']))
def info():
    """Gets the info."""
    myLogger.debug(ENTER)
    ret = {'info': 'index.html => Info in HTML format'}
    myLogger.debug(EXIT)
    return jsonify(ret)
