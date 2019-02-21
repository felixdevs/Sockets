""" Запуск простого сервера на сокетах
 - однопоточный. если один клиент подключился - друго ответы от сервера получить не может"""
import socket

# domain:5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # для возможности переиспользования порта если мы его остановим
server_socket.bind(('localhost', 5000))  # указываем к какому домену и порту мы его превяжем
server_socket.listen()  # слушает

while True:
    print('Before .accept()')
    client_socket, addr = server_socket.accept()  # принимаем адресс клиента
    print('Connection from', addr)

    while True:
        # print('Before .recv()')
        request = client_socket.recv(4096)

        if not request:
            break
        else:
            response = 'Hello world\n'.encode()
            client_socket.send(response)

    print('Outside inner while loop')
    client_socket.close()
