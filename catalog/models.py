from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    photo = models.FileField(upload_to='uploads/')
    def __str__(self):
        return self.name

#implement model for shopping cart
class ShoppingCart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username
    
    
class DeliveryAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.TextField()
    def __str__(self):
        return self.user.username

class ShoppingOrder(models.Model):
    PAYMENT_OPTIONS = [
        ('0','Cash on delivery'),
        ('1','e-sewa'),
        ('2','Khalti')    
    ]
    STATUS_CHOICES = [
        ('0','Paid'),
        ('1','PENDING')    
    ]
    DELIVERY_CHOICES = [
        ('0','Not Delivered'),
        ('1','In Transit'),
        ('2','DELIVERED')    
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.ForeignKey(DeliveryAddress,on_delete=models.CASCADE,blank=True,null=True)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    payment_mode = models.TextField(choices=PAYMENT_OPTIONS,blank=True,null=True)
    paid_amount = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    payment_status = models.TextField(choices=STATUS_CHOICES,blank=True,null=True)
    delivery_status = models.TextField(choices=DELIVERY_CHOICES,blank=True,null=True)
    def __str__(self):
        return self.user.username 

class OrderItem(models.Model):
    orders = models.ForeignKey(ShoppingOrder,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    def __str__(self):
        return self.orders.user.username


    





# orders 

# orderID 
# user 
# totalAmount 
# modeofpayment: e-sewa,khalt,fonepay,cash on delivery
# paymentstatus : paid, pending
# orderstatus : delivered, pending , intransit 


# orderItems

# orderid  
# product