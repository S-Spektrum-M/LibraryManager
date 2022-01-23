"""
Web frontend
"""
from requests import get
from flask import Flask, render_template, request

APP = Flask(__name__)


@APP.route('/search')
def search():
    """
    Search
    """
    search_type = str(request.args.get('search_type')).lower().strip()
    search_term = str(request.args.get('search_term')).lower().strip()
    search_types = ['section', 'subsection', 'title', 'isbn', 'author']
    if search_type in search_types:
        status = get(
            f'http://localhost:5000/search?field={search_type}&info={search_term}'
        ).json()
        print(status)
        if 'error' not in status:
            return render_template('search.html', status=status['message'][0]['title'])
    return f"{search_type} is not valid try: {search_types}"


@APP.route('/')
def index():
    """
    Index page
    """
    return render_template('index.html')
