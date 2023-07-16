#include <sys/socket.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <arpa/inet.h>
#include <string.h>


#define SERVER_IP "localhost"
#define SERVER_PORT 8877
#define HISTOGRAM_SIZE 100

int main() {
    struct sockaddr_in server_address;
    memset(&server_address, 0, sizeof(server_address));
    server_address.sin_family = AF_INET;
    int k = 10000;
    long int response_time;
    
    inet_pton(AF_INET, SERVER_IP, &server_address.sin_addr);
    server_address.sin_port = htons(SERVER_PORT);
    int counter;
    int histogram[HISTOGRAM_SIZE] = {0};
    const char * message = "Hello!";
    struct timespec start_time, end_time;

    int client_socket = socket(PF_INET, SOCK_DGRAM, 0);
    if (client_socket < 0) {
        perror("Could not create socket!");
        exit(1);
    }
    printf("I'm before...\n");
    while(k){
        clock_gettime(CLOCK_MONOTONIC, &start_time);
        sendto(client_socket, message, strlen(message), 0, (struct sockaadr *)&server_address, sizeof(server_address));
        printf("I've sent...\n");
        if(recvfrom(client_socket, &counter, sizeof(counter), 0, NULL, NULL) < 0){
            printf("Ne polucheno");
            return 1;
        };
        printf("I've recieved...\n");
        clock_gettime(CLOCK_MONOTONIC, &end_time);
        
        
        response_time = 1000000 * (end_time.tv_sec - start_time.tv_sec) + (end_time.tv_nsec - start_time.tv_nsec)/1000;
        if(response_time >= 0 && response_time <= 99)++histogram[0];
        if(response_time >= 100 && response_time <= 199)++histogram[1];
        if(response_time >= 200 && response_time <= 299)++histogram[2];
        if(response_time >= 300 && response_time <= 399)++histogram[3];
        if(response_time >= 400 && response_time <= 499)++histogram[4];
        if(response_time >= 500 && response_time <= 599)++histogram[5];
        if(response_time >= 600 && response_time <= 699)++histogram[6];
        if(response_time >= 700 && response_time <= 799)++histogram[7];
        if(response_time >= 800 && response_time <= 899)++histogram[8];
        if(response_time >= 900 && response_time <= 999)++histogram[9];
        
        printf("Counter is %d\n", counter);
        printf("Response_time is %ld\n", response_time);
        --k;
    }

    for(int i = 0; i < 100; i++){
        printf("On interval %d is %d\n", i+1, histogram[i]);
    }
    close(client_socket);

    return 0;
}