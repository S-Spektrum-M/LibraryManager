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

def add_book(code):
    status = get(f'{uri}/add?code={code}').json()
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
    init('https://c84d-73-71-55-203.ngrok.io')
    while True:
        print('commands: checkout, return, add, owner, list')
        command = input('command: ')
        if command == 'checkout':
            code = input('code: ')
            name = input('name: ')
            print(checkout(code, name))
        elif command == 'return':
            code = input('code: ')
            print(return_book(code))
        elif command == 'add':
            code = input('code: ')
            print(add_book(code))
        elif command == 'owner':
            code = input('code: ')
            print(owner(code))
        elif command == 'exit':
            break
        elif command == 'list':
            list_books()
        else:
            print('invalid command')

if __name__ == '__main__':
    main()
