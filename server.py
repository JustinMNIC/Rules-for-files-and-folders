# на примере python разбираем как работают сокеты
import socket
from credentials import HOST, PORT, EXIT_MSG

server = socket.socket() #отвечает за серверное взаимедойствие, создаётся сокет

server.bind((HOST, PORT)) # принимает кортеж, закрепляет созданный сокет за соединением

server.listen() # слушает входящее соединение
print(f'Запущен сервер {HOST}:{PORT}')

client, address = server.accept() # блокирующий метод
print(f'Подключение от :{address}')

while True: # делаем бесконечный цикл для приёма чисел, и возврата их
    msg = client.recv(1024).decode() # получение сообщения от сокета
    # decode - из байт в строку
    # print(f'Сообщение от {address}: {msg}')
    if msg == EXIT_MSG:
        break
    try:
        num = float(msg) # принимаем число
    except ValueError:
        response = f'Отправляйте числа, а не <{msg}>' # обрабатываем ошибку
    else:
        response = str(num ** 2) # возращаем квадрат

    client.send(response.encode()) # когда получаем указываем сколько байти получаем, когда отправлеям уже известно сколько байт

server.close() # закрывается, порт, сокет и файловый дескриптор

