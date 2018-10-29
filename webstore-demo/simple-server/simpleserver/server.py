from flask import Blueprint, render_template

bp = Blueprint('simpleserver', __name__)


@bp.route('/')
def index():
    """Show index.html."""
    return render_template('index.html')
