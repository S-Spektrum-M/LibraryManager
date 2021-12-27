from requests import get

uri = str()


def init(url):
    global uri
    uri = url


def checkout(code, name):
    status = get(f'{uri}/checkout?data={code},{name}').json()
    if 'error' not in status:
        return status['message']
    return status['error']


def return_book(code):
    status = get(f'{uri}/return?code={code}').json()
    if 'error' not in status:
        return status['message']
    return status['error']


def add_book(code, title, author, section, subsection):
    status = get(f'{uri}/add?data={code},{title},{author},{section},{subsection}').json()
    if 'error' not in status:
        return status['message']
    return status['error']


def owner(code):
    status = get(f'{uri}/owner?code={code}').json()
    if 'error' not in status:
        return status['message']
    return status['error']


def list_books():
    book_list = get(f'{uri}/list').json()
    for code in book_list:
        print(f'{code} - {book_list[code]}')


def main():
    init('http://fbb8-73-71-55-203.ngrok.io')
    while True:
        print('commands: c-heckout, r-eturn, a-dd, o-wner, l-ist, q-uit')
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
        else:
            print('invalid command')


if __name__ == '__main__':
    main()
