#include <sys/types.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>

#define DEVICE_PATH "/dev/example"

int main(){
    int fd = open(DEVICE_PATH, O_RDWR | O_NONBLOCK);
    if(fd < 0){
        perror("Failed to open the device");
        return -1;
    }
    
    const char * message = "Privet";
    ssize_t bytesWrite = write(fd, message, strlen(message)); 
    if(bytesWrite < 0){
        perror("Failed to write to the device");
        return -1;
    }
    printf("Written %zd bytes: %s\n", bytesWrite, message);
    close(fd);
}