# tcp - port
# ip - Ip-address
#
# ip-address: 5000 - socket
# Asynchrony/socket/views.py
import socket
from Socket.views import *

URLS = {
    '/': index,
    '/blog': blog,
}


def parse_request(request):
    """ функция для извлечения GET и URL
        из запроса - b'GET / HTTP/1.1\r\nHost: localhost:5000\r\nUser-Agent: Mozilla/5.0 ...
    """
    parsed = request.split(' ')
    method = parsed[0]
    url = parsed[1]
    return method, url


def generate_headers(method, url):
    """ Проверяем на наличие GET и url"""
    if not method == 'GET':
        return 'HTTP/1.1 405 Method not allowed\n\n', 405

    if url not in URLS:
        return 'HTTP/1.1 404 Not found\n\n', 404

    return 'HTTP/1.1 200 OK\n\n', 200


def generate_content(code, url):
    if code == 404:
        return '<h1>404</h1><p>Not found</p>'
    if code == 405:
        return '<h1>405</h1><p>Method not allowed</p>'
    return URLS[url]()


def generate_responce(request):
    method, url = parse_request(request)
    headers, code = generate_headers(method, url)
    body = generate_content(code, url)
    return (headers + body).encode()


def run():
    # Серверная часть которая слушает, реагирует и обрабатывает (сервер)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем экземпляр
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # используется для избежания блокировки
    server_socket.bind(('localhost', 5000))  # ip-addres и port на котором работает сервер
    server_socket.listen()  # запуск сервера на получение запросов

    while True:
        client_socket, addr = server_socket.accept()  # тот кто шлет запрос (клиент)
        request = client_socket.recv(1024)  # то что приходит от клиента

        # print(request.decode('utf-8'))  # более презентабельный вывод
        print('-------------------------')
        print(request)  # печатаем запрос который пришел от клиента
        print(addr)     # его socket
        print('-------------------------')


        response = generate_responce(request.decode('utf-8'))  # подготовка ответа клиенту на его запрос

        client_socket.sendall(response)  # отправляем ответ от представления
        client_socket.close()            # закрываем соединение


if __name__ == '__main__':
    run()
