#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <fcntl.h>

#define SERVER_PORT 8080
#define BUFFER_SIZE 1024
#define DEVICE_PATH "/dev/mydevice"

int main() {
    int serverSocket, clientSocket;
    struct sockaddr_in serverAddr, clientAddr;
    socklen_t clientAddrLen;
    char buffer[BUFFER_SIZE];
    int deviceFile;
    ssize_t bytesRead;

    // Создание сокета
    serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSocket < 0) {
        perror("Ошибка при создании сокета");
        exit(1);
    }

    // Настройка адреса сервера
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    serverAddr.sin_port = htons(SERVER_PORT);

    // Привязка сокета к адресу сервера
    if (bind(serverSocket, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) < 0) {
        perror("Ошибка при привязке сокета к адресу сервера");
        exit(1);
    }

    // Ожидание подключения клиента
    if (listen(serverSocket, 1) < 0) {
        perror("Ошибка при ожидании подключения клиента");
        exit(1);
    }

    printf("Сервер запущен и ожидает подключения клиента...\n");

    // Принятие подключения от клиента
    clientAddrLen = sizeof(clientAddr);
    clientSocket = accept(serverSocket, (struct sockaddr *)&clientAddr, &clientAddrLen);
    if (clientSocket < 0) {
        perror("Ошибка при принятии подключения от клиента");
        exit(1);
    }

    printf("Подключение от клиента %s:%d\n", inet_ntoa(clientAddr.sin_addr), ntohs(clientAddr.sin_port));

    // Открытие символьного устройства
    deviceFile = open(DEVICE_PATH, O_RDONLY);
    if (deviceFile < 0) {
        perror("Ошибка при открытии символьного устройства");
        exit(1);
    }

    // Чтение данных из символьного устройства
    bytesRead = read(deviceFile, buffer, BUFFER_SIZE);
    if (bytesRead < 0) {
        perror("Ошибка при чтении данных из символьного устройства");
        exit(1);
    }

    // Отправка ответа клиенту
    if (send(clientSocket, buffer, bytesRead, 0) < 0) {
        perror("Ошибка при отправке ответа клиенту");
        exit(1);
    }

    // Закрытие символьного устройства
    close(deviceFile);

    // Закрытие сокетов
    close(clientSocket);
    close(serverSocket);

    return 0;
}
