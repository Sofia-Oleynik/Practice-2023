#include <sys/types.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include </home/sofia/src/ioctl/app/driver/my_ioctl.h>

#define DEVICE_PATH "/dev/ioctl"

int main(){
    int fd = open(DEVICE_PATH, O_RDWR);
    if(fd < 0){
        perror("Failed to open the device");
        return -1;
    }
    
    int user_counter;
    ioctl(fd, IOC_GET, &user_counter); 
    if(user_counter < 0){
        perror("Failed to get from the device");
        return -1;
    }
    printf("Counter is %d\n", user_counter);
    close(fd);
}