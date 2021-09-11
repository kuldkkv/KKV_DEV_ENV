/*
 * chardev.c: Creates a read-only/dummy charcter device
 */

#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <asm/uaccess.h>

#define MOD_AUTHOR "Kuldeep K Verma <kuld.kkv@gmail.com>"
#define MOD_DESC "A simple module"

/*
 * Prototypes
 */

int mod_init(void);
void mod_exit(void);
static int device_open(struct inode *, struct file *);
static int device_release(struct inode *, struct file *);
static ssize_t device_read(struct file *, char *, size_t, loff_t *);
static ssize_t device_write(struct file *, const char *, size_t, loff_t *);

#define SUCCESS 0
#define DEVICE_NAME "chardev"
#define BUFLEN 80

/*
 * Global variable declared as static so are global within this file.
 */

static int major_device_number = 0;
static int is_device_open = 0;
static char buffer[BUFLEN];
static char *buffer_ptr;
static struct file_operations fops = {
	.read = device_read,
	.write = device_write,
	.open = device_open,
	.release = device_release
};

/*
 * Function definations.
 */

int mod_init(void)
{
	major_device_number = register_chrdev(0, DEVICE_NAME, &fops);
	if (major_device_number < 0) {
		printk(KERN_ALERT "%s: registering device failed with %d\n",
		       DEVICE_NAME, major_device_number);
		return major_device_number;
	}
	printk(KERN_ALERT "%s: major device number assigned [%d]\n",
	       DEVICE_NAME, major_device_number);
	printk(KERN_ALERT
	       "%s: create device file as: 'mknod /dev/hello c %d 0'\n",
	       DEVICE_NAME, major_device_number);
	printk(KERN_ALERT "%s: try to cat and echo to this device.\n",
	       DEVICE_NAME);
	printk(KERN_ALERT "%s: remove the device and module when done.\n",
	       DEVICE_NAME);

	return SUCCESS;
}

void mod_exit(void)
{
	/*
	 * unregister device
	 */

	unregister_chrdev(major_device_number, DEVICE_NAME);
	printk(KERN_ALERT "%s: device unregistered and module\n", DEVICE_NAME);
}

module_init(mod_init);
module_exit(mod_exit);
MODULE_LICENSE("GPL");
MODULE_AUTHOR(MOD_AUTHOR);
MODULE_DESCRIPTION(MOD_DESC);

/*
 * Device methods.
 */

static int device_open(struct inode *inode, struct file *filp)
{
	static int open_counter = 1;
	if (is_device_open)
		return -EBUSY;
	++is_device_open;
	sprintf(buffer, "device opened %d times.\n", open_counter++);
	buffer_ptr = buffer;
	try_module_get(THIS_MODULE);

	return SUCCESS;
}

static int device_release(struct inode *inode, struct file *filp)
{
	--is_device_open;
	module_put(THIS_MODULE);

	return SUCCESS;
}

static ssize_t
device_read(struct file *filp, char *buff, size_t length, loff_t * offset)
{
	int bytes_written = 0;

	if (*buffer_ptr == 0)
		return 0;

	while (length && *buffer_ptr) {
		put_user(*(buffer_ptr++), buff++);
		length--;
		bytes_written++;
	}

	return bytes_written;
}

static ssize_t
device_write(struct file *filp, const char *buff, size_t length,
	     loff_t * offset)
{
	printk(KERN_ALERT "%s: sorry, operation not permitted.\n", DEVICE_NAME);
	return -EINVAL;
}
