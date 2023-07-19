import socket

s_m = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = 'localhost'
port_m = 54321 # порт для сообщений

s_m.connect((host, port_m))

while True:
    
    msg_data = s_m.recv(1024)
    message = msg_data.decode()
    if message:
        print('Received message:', message)
    

# Закрываем соединение и окна OpenCV
s_m.close()

