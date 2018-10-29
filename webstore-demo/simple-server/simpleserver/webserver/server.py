from flask import Blueprint, render_template, jsonify

bp = Blueprint('simpleserver', __name__)


@bp.route('/')
def index():
    """Show index.html."""
    return render_template('index.html')


@bp.route('/info', methods=(['GET']))
def info():
    """Gets the info."""
    ret = {'info': 'index.html => Info in HTML format'}
    return jsonify(ret)
