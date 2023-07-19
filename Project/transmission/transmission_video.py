import cv2
import socket
import struct
import pickle


s_v = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port_v = 12345 # порт для видеопотока
s_v.connect((host, port_v))

while True:

    data = b''
    size = struct.calcsize('L')
    while len(data) < size:
        data += s_v.recv(4096)
    packed_size = data[:size]
    data = data[size:]
    msg_size = struct.unpack('L', packed_size)[0]
    while len(data) < msg_size:
        data += s_v.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)

    cv2.imshow('Received frame', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Закрываем соединение и окна OpenCV
s_v.close()
cv2.destroyAllWindows()
