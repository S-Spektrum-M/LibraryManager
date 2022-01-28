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
            for code in status:
                response_str.append(f"{code}: {status[code]['title']}")
            if len(response_str) > 0:
                return render_template('search.html', status=response_str)
            return render_template('search.html', status=["No Books Found"])
        print(status['error'])
    bnf = f"{search_type} is not valid try: {search_types}"
    return render_template('search.html', status=[bnf])


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


@APP.route('/add', methods=['POST'])
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

@APP.route('/checkout')
def checkout():
    """
    Checkout book
    """
    return render_template('checkout.html')

@APP.route('/checkout', methods=['POST'])
def checkout_book():
    """
    checkout_book
    """
    status = get(
        f'http://localhost:5000/checkout?data={str(request.form.get("code"))},{request.form.get("user_id")}'
    ).json()
    if 'error' not in status:
        return render_template('checkout.html', message=status['message'])
    return render_template('checkout.html', error=status['error'])

@APP.route('/return')
def return_book():
    """
    Return book
    """
    return render_template('return.html')

@APP.route('/return', methods=['POST'])
def return_page():
    """
    Return book
    """
    status = get(
        f'http://localhost:5000/return?code={str(request.form.get("code"))}'
    ).json()
    if 'error' not in status:
        return render_template('return.html', message=status['message'])
    return render_template('return.html', error=status['error'])

@APP.route('/')
def index():
    """
    Index page
    """
    return render_template('index.html')
