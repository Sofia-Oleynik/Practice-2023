
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <time.h>

#define SERVER_IP "127.0.0.1"
#define SERVER_PORT 8080
#define BUFFER_SIZE 1024

int main() {
    int clientSocket;
    struct sockaddr_in serverAddr;
    char buffer[BUFFER_SIZE];
    time_t startTime, endTime;

    // Создание сокета
    clientSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (clientSocket < 0) {
        perror("Ошибка при создании сокета");
        exit(1);
    }

    // Настройка адреса сервера
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(SERVER_PORT);
    if (inet_pton(AF_INET, SERVER_IP, &(serverAddr.sin_addr)) <= 0) {
        perror("Ошибка при настройке адреса сервера");
        exit(1);
    }

    // Подключение к серверу
    if (connect(clientSocket, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) < 0) {
        perror("Ошибка при подключении к серверу");
        exit(1);
    }

    // Отправка запроса
    snprintf(buffer, BUFFER_SIZE, "Привет, сервер!");
    startTime = time(NULL);
    if (send(clientSocket, buffer, strlen(buffer), 0) < 0) {
        perror("Ошибка при отправке запроса");
        exit(1);
    }

    // Получение ответа
    memset(buffer, 0, BUFFER_SIZE);
    if (recv(clientSocket, buffer, BUFFER_SIZE, 0) < 0) {
        perror("Ошибка при получении ответа");
        exit(1);
    }
    endTime = time(NULL);

    // Вывод времени получения ответа
    printf("Время получения ответа от сервера: %ld секунд\n", endTime - startTime);

    // Закрытие сокета
    close(clientSocket);

    return 0;
}
