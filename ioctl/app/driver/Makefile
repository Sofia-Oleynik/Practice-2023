obj-m += my_ioctl.o
#my_ioctl.o: my_ioctl.h

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules
clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
test:
	sudo insmod my_ioctl.ko
	sudo dmesg
