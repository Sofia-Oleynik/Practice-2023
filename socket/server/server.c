#include <sys/socket.h>
#include <sys/types.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <stdbool.h>
#include <sys/ioctl.h>
#include <my_ioctl.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#define BUFFER_SIZE 1024
#define SERVER_PORT 8877
#define DEVICE_PATH "/dev/ioctl"

int main(int argc, char *argv[]){
    int server_socket, client_socket;
    struct sockaddr_in server_address, client_address;
    int client_address_len = 0;
    memset(&server_address, 0, sizeof(server_address));
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(SERVER_PORT);
    server_address.sin_addr.s_addr = htonl(INADDR_ANY);
    int response;
    int device_file;

    server_socket = socket(PF_INET, SOCK_DGRAM, 0);
    if(server_socket < 0) {
        perror("Socket error!");
        return 1;
    } 

    if(bind(server_socket, (struct sockaddr *)&server_address, sizeof(server_address)) < 0){
        perror("Privyzka error!");
        return 1;
    }

    device_file = open(DEVICE_PATH, O_RDONLY);
    if(device_file < 0){
        perror("Open device file error: ");
        return 1;
    }
    printf("I'm before...\n");
    while(true){
        char buffer[500];
        recvfrom(server_socket, buffer, sizeof(buffer), 0, (struct sockaddr *)&client_address, &client_address_len);
        printf("I've recieved %s\n", buffer);
        ioctl(device_file, IOC_GET, &response);
        printf("I've red...%d\n", response);
        sendto(server_socket, &response, sizeof(int), 0, (struct sockaddr *)&client_address, sizeof(client_address));
        printf("I've sent...\n");
    }

    close(server_socket);
    return 0;
}