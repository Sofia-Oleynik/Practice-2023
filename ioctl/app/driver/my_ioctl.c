#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/wait.h>
#include <linux/delay.h>
#include <linux/kthread.h>
#include <asm/uaccess.h>
#include </home/sofia/src/ioctl/app/driver/my_ioctl.h>

MODULE_LICENSE("GPL");
#define DEVICE_NAME "ioctl"

static int device_open(struct inode *, struct file *);
static int device_release(struct inode *, struct file *);
static inline long device_unlocked_ioctl(struct file *, unsigned int, unsigned long);
static int device_open_count = 0;
static int major_num;
static int counter = 0;
struct task_struct *ts;

static struct file_operations file_ops = {
 .unlocked_ioctl = device_unlocked_ioctl,
 .open = device_open,
 .release = device_release
};

static int device_open(struct inode *inode, struct file *file) {
 /*
 if (device_open_count) {
 return -EBUSY;
 }*/
 
 device_open_count++;
 try_module_get(THIS_MODULE);
 return 0;
}

static int device_release(struct inode *inode, struct file *file) {
 
 device_open_count--;
 module_put(THIS_MODULE);
 return 0;
}

static int my_thread(void *data){
    while(1){
        ++counter;
        msleep(1000);
        if(kthread_should_stop())break;
    }
    return 0;
}

static inline long device_unlocked_ioctl(struct file *file, unsigned int cmd, unsigned long arg){
 switch(cmd){
    case IOC_RESET:
    counter = 0;
    break;
    case IOC_GET:
    copy_to_user(arg, &counter, sizeof(counter));
    break;
    default:
    return -ENOTTY;
 }
 return counter;
}

static int __init ioctl_init(void) {
 ts = kthread_run(my_thread, NULL, "Kthread run!");
 major_num = register_chrdev(0, DEVICE_NAME, &file_ops);
 if (major_num < 0) {
 printk(KERN_ALERT "Could not register device: %d\n", major_num);
 return major_num;
 } else {
 printk(KERN_INFO "ioctl module loaded with device major number %d\n", major_num);
 return 0;
 }
}
static void __exit ioctl_exit(void) {
 kthread_stop(ts);
 unregister_chrdev(major_num, DEVICE_NAME);
 printk(KERN_INFO "Goodbye, World!\n");
}

module_init(ioctl_init);
module_exit(ioctl_exit);