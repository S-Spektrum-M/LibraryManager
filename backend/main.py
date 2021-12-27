"""
./README.md
"""
import json
import flask
from flask import request, jsonify

APP = flask.Flask(__name__)


@APP.route('/list', methods=['GET'])
def list():
    """
    list all available books
    """
    FILE = open('dbs/books.json', 'r')
    BOOKS = json.load(FILE)
    FILE.close()
    return jsonify(BOOKS), 200

@APP.route('/add', methods=['GET'])
def add_book():
    FILE = open('dbs/books.json', 'r')
    BOOKS = json.load(FILE)
    FILE.close()
    """
    Add a book to the database
    url/add?code=<code>
    """
    if 'code' in request.args:
        code = request.args['code']
        if code not in BOOKS:
            BOOKS[code] = {
                'available': True,
                'checked_out_by': 'none',
            }
            FILE = open('dbs/books.json', 'w')
            json.dump(BOOKS, FILE)
            FILE.close()
            return jsonify({'message': 'Book added'}), 200
        return {'error': 'Book already exists'}, 400
    return jsonify({'error': 'Missing Data'}), 400


@APP.route('/checkout', methods=['GET'])
def checkout():
    FILE = open('dbs/books.json', 'r')
    BOOKS = json.load(FILE)
    FILE.close()
    """
    url/checkout?data=<code>,<user>
    """
    if 'data' in request.args:
        data = request.args['data']
        data_list = data.split(',')
        if len(data_list) == 2:
            if data_list[0] in BOOKS:
                if BOOKS[data_list[0]]['available']:
                    BOOKS[data_list[0]]['available'] = False
                    BOOKS[data_list[0]]['checked_out_by'] = data_list[1]
                    FILE = open('dbs/books.json', 'w')
                    json.dump(BOOKS, FILE)
                    FILE.close()
                    return jsonify({'message': 'checked_out'}), 200
                return jsonify({'error': 'Book already checked out'}), 400
            return jsonify({'error': 'Book not found'}), 400
        return jsonify({'error': 'Missing Data'}), 400
    return jsonify({'error': 'Missing Data'}), 400


@APP.route('/return', methods=['GET'])
def return_book():
    FILE = open('dbs/books.json', 'r')
    BOOKS = json.load(FILE)
    FILE.close()
    """
    url/return?code=<code>
    """
    if 'code' in request.args:
        code = request.args['code']
        if not BOOKS[code]['available']:
            BOOKS[code]['available'] = True
            BOOKS[code]['checked_out_by'] = 'none'
            FILE = open('dbs/books.json', 'w')
            json.dump(BOOKS, FILE)
            FILE.close()
            return jsonify({'message': 'returned'}), 200
        return jsonify({'error': 'Book Not Checked Out'}), 400
    return jsonify({'error': 'Missing Data'}), 400


@APP.route('/owner', methods=['GET'])
def owner():
    FILE = open('dbs/books.json', 'r')
    BOOKS = json.load(FILE)
    FILE.close()
    """
    url/owner?code=<code>
    """
    if 'code' in request.args:
        code = request.args['code']
        if code in BOOKS:
            owner = BOOKS[code]['checked_out_by']
            if owner != 'none':
                return jsonify({'message': owner}), 200
            return jsonify({'error': 'Book Not Checked Out'}), 400
        return jsonify({'error': 'Book Not Found'}), 400
    return jsonify({'error': 'Missing Data'}), 400


# @APP.route('/', methods=['GET'])
# @APP.route('/', methods=['GET'])
# @APP.route('/', methods=['GET'])
# @APP.route('/')
APP.run(host="localhost", port=8080)
