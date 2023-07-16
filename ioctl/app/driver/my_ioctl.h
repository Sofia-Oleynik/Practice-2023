#ifndef __MYDRIVERIO_H__
#define __MYDRIVERIO_H__
#include <linux/ioctl.h>
#define MAGIC_NUM 0xF1
#define IOC_GET _IOR(MAGIC_NUM, 0, int)
#define IOC_RESET _IO(MAGIC_NUM, 1)
#endif __MYDRIVERIO_H__