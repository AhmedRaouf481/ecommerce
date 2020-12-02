from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    name = models.CharField(max_length=200, null=True)
    price = models.IntegerField(null=True)
    descreption = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='images/products', null=True , blank = True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    @property
    def imgUrl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):

    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    compelete = models.BooleanField(default=False, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
        


class OrderItem(models.Model):

    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=True, blank= True, choices=[(x, x) for x in range(1, 100)])
    # quantity = models.IntegerField(default=0, null=True, blank= True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShipingAddress(models.Model):
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    Address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True)
    Zipcode = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.Address
    

