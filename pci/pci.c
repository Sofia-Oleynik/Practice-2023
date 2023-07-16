#include <linux/init.h>
#include <linux/module.h>
#include <linux/pci.h>
#include <linux/kernel.h>
#include <linux/ioctl.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/device.h>
#include <linux/uaccess.h>
#include <linux/io.h>

#define MY_DRIVER "my_pci_driver"
#define CLASS_NAME "pci_class"
#define MAC_ADDR_OFFSET 0x10

#define VENDOR_ID 8086
#define PRODUCT_ID 2829

static dev_t dev;
static struct cdev cdev;
static struct class *device_class;
static struct device *device;

static int major;

static struct pci_device_id my_driver_id_table[] = {
	{PCI_DEVICE(VENDOR_ID, PRODUCT_ID) },
	{0,}
};

MODULE_DEVICE_TABLE(pci, my_driver_id_table);

static int my_driver_probe(struct pci_dev *, const struct pci_device_id *);
static void my_driver_remove(struct pci_dev *);
static int pci_driver_open(struct inode *, struct file *);
static int pci_driver_release(struct inode *, struct file *);
static long pci_driver_ioctl(struct file *, unsigned int , unsigned long );

static struct pci_driver my_driver = {
	.name = MY_DRIVER,
	.id_table = my_driver_id_table,
	.probe = my_driver_probe,
	.remove = my_driver_remove
};

static const struct file_operations pci_driver_fops = {
	.owner = THIS_MODULE,
	.open = pci_driver_open,
	.release = pci_driver_release,
	.unlocked_ioctl = pci_driver_ioctl,
};

static int __init pci_driver_init(void)
{
	return pci_register_driver(&my_driver);
}

static int pci_driver_open(struct inode *inode, struct file *filp){
	struct pci_dev *pdev;
	pdev = pci_get_device(VENDOR_ID, PRODUCT_ID, NULL);
	if(!pdev){
		pr_err("Failed to get PCI device\n");
		return -ENODEV;
	}

	filp->private_data = pdev;
	return 0;
}

static int pci_driver_release(struct inode *inode, struct file *filp){
	
	filp->private_data = NULL;
	return 0;
}

static long pci_driver_ioctl(struct file *filp, unsigned int cmd, unsigned long arg)
{
	struct pci_dev *pdev = filp->private_data;
	u8 mac_addr[ETH_ALEN];
	void __iomem *base_addr;
	int ret;

	if(cmd!=IOCTL_GET_MAC_ADDR)
	{
		return -EINVAL;
	}

	base_addr = ioremap_nocache(pci_resource_start(pdev, 0) + MAC_ADDR_OFFSET, ETH_ALEN);
	if(!base_addr){
		pr_err("Failed to map IO memory\n");
		return -EFAULT;
	}
	
	memcpy_fromio(mac_addr, base_addr, ETH_ALEN);

	ret = copy_to_user((void __user *)arg, mac_addr, ETH_ALEN);
	if(ret){
		pr_err("Failed to copy MAC address to user\n");
		retutn -EFAULT;
	}

	iounmap(base_addr);
	return 0;
}

static void __exit pci_driver_exit(void)
{
    pci_unregister_driver(&my_driver);
}

static int my_driver_probe(struct pci_dev *pdev, const struct pci_device_id *id)
{
	int ret;

	ret = pci_enable_device(pdev);
	if(ret){
		dev_err(&pdev->dev, "Failed to enable PCI device\n");
		return ret;
	}

	pci_set_master(pdev);
	pci_read_config_byte(pdev, PCI_CLASS_DEVICE, &class);
	if(class != PCI_CLASS_NETWORK_ETHERNET){
		dev_err(&pdev->dev, "Not a network Ethernet device");
		return -ENODEV;
	}

	ret = alloc_chrdev_region(&dev, 0, 1, MY_DRIVER);
	if(ret < 0){
		dev_err(&pdev->dev, "Failed to allocate device number\n");
		return ret;
	}

	cdev_init(&cdev, &pci_driver_fops);
	cdev_add(&cdev, dev, 1);

	device_class = class_create(THIS_MODULE, CLASS_NAME);
	if(IS_ERR(device_class)){
		unregister_chrdev_region(dev, 1);
		return PTR_ERR(device_class);
	}

	device = device_create(device_class, NULL, dev, NULL, MY_DRIVER);
	if(IS_ERR(device)){
		class_destroy(device_class);
		unregister_chrdev_region(dev, 1);
		return PTR_ERR(device);
	}

	return 0;
}

static void my_driver_remove(struct pci_dev *pdev)
{
	device_destroy(device_class, dev);
	class_destroy(device_class);
	unregister_chrdev_region(dev, 1);
	pci_disable_device(pdev);
}

MODULE_LICENSE("GPL");

module_init(pci_driver_init);
module_exit(pci_driver_exit);