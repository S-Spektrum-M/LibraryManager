"""
./README.md
"""
import json
import flask
from flask import request, jsonify

APP = flask.Flask(__name__)


@APP.route('/list', methods=['GET'])
def list_books():
    """
    list all available books
    """
    file = open('dbs/books.json', 'r')
    book_dict = json.load(file)
    file.close()
    return jsonify(book_dict), 200


@APP.route('/add', methods=['GET'])
def add_book():
    """
    Add a book to the database
    url/add?data=<code>,<title>,<author>,<section>,<subsection>
    """
    file = open('dbs/books.json', 'r')
    book_dict = json.load(file)
    file.close()
    if 'data' in request.args:
        data = request.args['data']
        data = data.split(',')
        if len(data) == 5:
            code = data[0]
            if code not in book_dict:
                book_dict[code] = {
                    'available': True,
                    'checked_out_by': 'none',
                    'title': data[1],
                    'author': data[2],
                    'section': data[3],
                    'subsection': data[4]
                }
                file = open('dbs/books.json', 'w')
                json.dump(book_dict, file)
                file.close()
                return jsonify({'message': 'Book added'}), 200
            return jsonify({'message': 'Book already exists'}), 400
        return jsonify({'error': 'Missing Data'}), 400
    return jsonify({'error': 'no data'}), 400


@APP.route('/checkout', methods=['GET'])
def checkout():
    """
    url/checkout?data=<code>,<user>
    """
    file = open('dbs/books.json', 'r')
    book_dict = json.load(file)
    file.close()
    if 'data' in request.args:
        data = request.args['data']
        data_list = data.split(',')
        if len(data_list) == 2:
            if data_list[0] in book_dict:
                if book_dict[data_list[0]]['available']:
                    book_dict[data_list[0]]['available'] = False
                    book_dict[data_list[0]]['checked_out_by'] = data_list[1]
                    file = open('dbs/books.json', 'w')
                    json.dump(book_dict, file)
                    file.close()
                    return jsonify({'message': 'checked_out'}), 200
                return jsonify({'error': 'Book already checked out'}), 400
            return jsonify({'error': 'Book not found'}), 400
        return jsonify({'error': 'Missing Data'}), 400
    return jsonify({'error': 'Missing Data'}), 400


@APP.route('/return', methods=['GET'])
def return_book():
    """
    url/return?code=<code>
    """
    file = open('dbs/books.json', 'r')
    book_dict = json.load(file)
    file.close()
    if 'code' in request.args:
        code = request.args['code']
        if code in book_dict:
            if not book_dict[code]['available']:
                book_dict[code]['available'] = True
                book_dict[code]['checked_out_by'] = 'none'
                file = open('dbs/books.json', 'w')
                json.dump(book_dict, file)
                file.close()
                return jsonify({'message': 'returned'}), 200
            return jsonify({'error': 'Book Not Checked Out'}), 400
        return jsonify({'error':'Book does not exist'}), 400
    return jsonify({'error': 'Missing Data'}), 400


@APP.route('/owner', methods=['GET'])
def get_owner():
    """
    url/owner?code=<code>
    """
    file = open('dbs/books.json', 'r')
    book_dict = json.load(file)
    file.close()
    if 'code' in request.args:
        code = request.args['code']
        if code in book_dict:
            owner = book_dict[code]['checked_out_by']
            if owner != 'none':
                return jsonify({'message': owner}), 200
            return jsonify({'error': 'Book Not Checked Out'}), 400
        return jsonify({'error': 'Book Not Found'}), 400
    return jsonify({'error': 'Missing Data'}), 400


@APP.route('/search', methods=['GET'])
def search():
    """
    url/search?field=<field>&info=<info>
    """
    file = open('dbs/books.json', 'r')
    book_dict = json.load(file)
    file.close()
    field = request.args['field']
    info = request.args['info']
    if field in ['section', 'subsection', 'title', 'isbn', 'author']:
        ret_list = []
        for book in book_dict:
            if book_dict[book][field].lower() == info:
                ret_list.append(book_dict[book])
        return jsonify({'message': ret_list}), 200
    return jsonify({'error': 'Missing Data'}), 400

APP.run(host="localhost", port=5000)
