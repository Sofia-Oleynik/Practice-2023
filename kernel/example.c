#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/wait.h>
#include <asm/uaccess.h>

MODULE_LICENSE("GPL");

#define DEVICE_NAME "example"
#define MSG_BUFFER_LEN 10

static DECLARE_WAIT_QUEUE_HEAD(wq);
//static bool flag = true;

static int device_open(struct inode *, struct file *);
static int device_release(struct inode *, struct file *);
static ssize_t device_read(struct file *, char *, size_t, loff_t *);
static ssize_t device_write(struct file *, const char *, size_t, loff_t *);
static int major_num;
static int device_open_count = 0;
static char msg_buffer[MSG_BUFFER_LEN] = "";

static int read_ptr = 0;
static int write_ptr = 0;

static struct file_operations file_ops = {
 .read = device_read,
 .write = device_write,
 .open = device_open,
 .release = device_release
};

static ssize_t device_read(struct file *flip, char *buffer, size_t len, loff_t * offset) {
 int bytes_read = 0;
 //wait_queue_head_t wq;
 //init_waitqueue_head(&wq);
 printk(KERN_INFO "Inside read\n");
 printk(KERN_INFO "Scheduling Out\n");
 wait_event_interruptible(wq, write_ptr != read_ptr);
 printk(KERN_INFO "Woken up\n");
 while (len && (msg_buffer[read_ptr] != '\0')) {
 
 put_user(msg_buffer[read_ptr], buffer++);
 len--;
 bytes_read++;
 read_ptr = (read_ptr + 1) % MSG_BUFFER_LEN;
 }
 
 
 return bytes_read;
}

static ssize_t device_write(struct file *flip, const char *buffer, size_t len, loff_t *offset) {
 int bytes_write = 0;
 if((write_ptr == read_ptr) && (flip->f_flags & O_NONBLOCK)){
 printk(KERN_INFO "Inside write\n");
 printk(KERN_INFO "Sheduling out inside write\n");
 
 while (len) {
 
 get_user(msg_buffer[write_ptr], buffer++);
 len--;
 bytes_write++;
 write_ptr = (write_ptr + 1) % MSG_BUFFER_LEN;
 }
 wake_up_interruptible(&wq);
 } else {
    printk(KERN_INFO "Blocking!");
 }
 
 return bytes_write;
}

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
static int __init example_init(void) {
 
 major_num = register_chrdev(0, DEVICE_NAME, &file_ops);
 if (major_num < 0) {
 printk(KERN_ALERT "Could not register device: %d\n", major_num);
 return major_num;
 } else {
 printk(KERN_INFO "example module loaded with device major number %d\n", major_num);
 return 0;
 }
}
static void __exit example_exit(void) {
 
 unregister_chrdev(major_num, DEVICE_NAME);
 printk(KERN_INFO "Goodbye, World!\n");
}

module_init(example_init);
module_exit(example_exit);