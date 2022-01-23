"""
Terminal frontend
"""
from requests import get

URI = str()


def _init(url):
    """
    Initialize the global URI variable
    """
    global URI
    URI = url


def checkout(code, name):
    """
    Checkout a book
    """
    status = get(f'{URI}/checkout?data={code},{name}').json()
    if 'error' not in status:
        return status['message']
    return status['error']


def return_book(code):
    """
    Return a book
    """
    status = get(f'{URI}/return?code={code}').json()
    if 'error' not in status:
        return status['message']
    return status['error']


def add_book(code, title, author, section, subsection):
    """
    Add a book
    """
    status = get(
        f'{URI}/add?data={code},{title},{author},{section},{subsection}').json(
        )
    if 'error' not in status:
        return status['message']
    return status['error']


def owner(code):
    """
    Get the owner of a book
    """
    status = get(f'{URI}/owner?code={code}').json()
    if 'error' not in status:
        return status['message']
    return status['error']


def list_books():
    """
    List all books
    """
    book_list = get(f'{URI}/list').json()
    for code in book_list:
        print(f'{code} - {book_list[code]}')


def search(field, info):
    """ Search for a book """
    status = get(f'{URI}/search?data={field},{info}').json()
    if 'error' not in status:
        return status['message']
    return status['error']


def main():
    """
    main function
    """
    _init('http://localhost:8080')
    while True:
        print(
            'commands: c-heckout, r-eturn, a-dd, o-wner, l-ist, q-uit, s-earch'
        )
        command = input('command: ')
        if command == 'c':
            code = input('code: ')
            name = input('name: ')
            print(checkout(code, name))
        elif command == 'r':
            code = input('code: ')
            print(return_book(code))
        elif command == 'a':
            code = input('code: ')
            title = input('title: ')
            author = input('author: ')
            section = input('section: ')
            subsection = input('subsection: ')
            print(add_book(code, title, author, section, subsection))
        elif command == 'o':
            code = input('code: ')
            print(owner(code))
        elif command == 'l':
            list_books()
        elif command == 'q':
            break
        elif command == 's':
            field = input('field: ')
            info = input('info: ')
            search_results = search(field, info)
            for search_result in search_results:
                print(search_result)
        else:
            print('invalid command')


if __name__ == '__main__':
    main()
