#include <sys/types.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>

#define DEVICE_PATH "/dev/example"

int main(){
    int fd = open(DEVICE_PATH, O_RDWR);
    if(fd < 0){
        perror("Failed to open the device");
        return -1;
    }
    
    char buffer[20];
    ssize_t bytesRead = read(fd, buffer, sizeof(buffer)); 
    if(bytesRead < 0){
        perror("Failed to read from the device");
        return -1;
    }
    printf("Read %zd bytes: %s\n", bytesRead, buffer);
    close(fd);
}