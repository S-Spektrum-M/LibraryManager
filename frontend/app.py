"""
Web frontend
"""
from requests import get
from flask import Flask, render_template, request

APP = Flask(__name__)


@APP.route('/result')
def result():
    """
    Search Result
    """
    search_type = str(request.args.get('search_type')).lower().strip()
    search_term = str(request.args.get('search_term')).lower().strip()
    search_types = ['section', 'subsection', 'title', 'isbn', 'author']
    if search_type in search_types:
        status = get(
            f'http://localhost:5000/search?field={search_type}&info={search_term}'
        ).json()
        if 'error' not in status:
            response_str = []
            status = status['message']
            print(status)
            for book in status:
                response_str.append(book['title'])
            if len(response_str) > 0:
                return render_template('result.html', status=response_str)
            return render_template('result.html', status=["No Books Found"])
        print(status['error'])
    return f"{search_type} is not valid try: {search_types}"


@APP.route('/search')
def search():
    """
    Book Search
    """
    return render_template('search.html')


@APP.route('/add')
def add():
    """
    Add books
    """
    return render_template('add.html')


@APP.route('/list')
def list_books():
    """
    List books
    """
    books = get('http://localhost:5000/list').json()
    book_list = []
    for book in books:
        book_list.append(f"{book} {books[book]['title']}")
    return render_template('list.html', book_list=book_list)


@APP.route('/addtodb', methods=['POST'])
def add_book():
    """
    Add book to database
    """
    code = request.form.get('code')
    title = request.form.get('title')
    author = request.form.get('author')
    section = request.form.get('section')
    subsection = request.form.get('subsection')
    status = get(
        f'http://localhost:5000/add?data={code},{title},{author},{section},{subsection}'
    ).json()
    if 'error' not in status:
        return render_template('add.html', message=status['message'])
    return render_template('add.html', error=status['error'])


@APP.route('/')
def index():
    """
    Index page
    """
    return render_template('index.html')
