""" Запуск  асинхронного сервера на сокетах
может отвечать одновременно многим клиентам"""
import socket
import selectors


selector = selectors.DefaultSelector()


def server():
    """ Определение серверного сокета """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # для возможности переиспользования порта если мы его остановим
    server_socket.bind(('localhost', 5000))  # указываем к какому домену и порту мы его превяжем
    server_socket.listen()  # запуск на прослушку

    selector.register(fileobj=server_socket,
                      events=selectors.EVENT_READ,
                      data=accept_connection)


# Принятие соединения от клиента
def accept_connection(server_socket):
        client_socket, addr = server_socket.accept()  # принимаем адресс клиента
        print('Connection from', addr)

        selector.register(fileobj=client_socket,
                          events=selectors.EVENT_READ,
                          data=send_massage)


# Получение от пользователя сообщения и отправка ему сообщения
def send_massage(client_socket):

        request = client_socket.recv(4096)

        if request:
            response = 'Hello world\n'.encode()
            client_socket.send(response)
        else:
            selector.unregister(client_socket)
            client_socket.close()


def event_loop():
    while True:

        events = selector.select()  # (key, events)
        for key, _ in events:
            callback = key.data
            callback(key.fileobj)


if __name__ == '__main__':
    server()
    event_loop()
