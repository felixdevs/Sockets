""" Запуск  асинхронного сервера на сокетах
может отвечать одновременно многи клиентам"""
import socket
from select import select

to_monitor = []  # константа для фалов select


# Определение серверного сокета

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # для возможности переиспользования порта если мы его остановим
server_socket.bind(('localhost', 5000))  # указываем к какому домену и порту мы его превяжем
server_socket.listen()  # запуск на прослушку


# Принятие соединения от клиента
def accept_connection(server_socket):
        client_socket, addr = server_socket.accept()  # принимаем адресс клиента
        print('Connection from', addr)

        to_monitor.append(client_socket)


# Получение от пользователя сообщения и отправка ему сообщения
def send_massage(client_socket):

        request = client_socket.recv(4096)

        if request:
            response = 'Hello world\n'.encode()
            client_socket.send(response)
        else:
            client_socket.close()


def event_loop():
    while True:
        # мониторит изменение состояния файлов - read, write, errors
        ready_to_read, _, _ = select(to_monitor, [], [])

        for sock in ready_to_read:
            if sock is server_socket:
                accept_connection(sock)
            else:
                send_massage(sock)


if __name__ == '__main__':
    to_monitor.append(server_socket)  # помещаем в список клиентский сокет
    event_loop()
