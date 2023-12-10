from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  email = models.EmailField(null=True, blank=True)


class Product(models.Model):
  name = models.CharField(max_length=150, null=True, blank=True)
  # id = models.IntegerField(primary_key=True)
  price = models.DecimalField(decimal_places=2, max_digits=7, default=0)
  image = models.ImageField(null=True, blank=True)
  digital = models.BooleanField(default=False, blank=True, null=True)

class Order(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
  transactionId = models.IntegerField(null=True, blank=True)
  date_added = models.DateTimeField(auto_now_add=True)
  complete = models.BooleanField(default=False)

  @property
  def shipping(self):
    items = self.orderitem_set.all()
    for item in items:
      shipping = None
      if item.product.digital == False:
        shipping = True
    return shipping

  def get_cart_total(self):
    total = 0
    items = self.orderitem_set.all()
    for item in items:
      total += item.get_item_total()
    return total

  def get_cart_items(self):
    total = 0
    items = self.orderitem_set.all()
    for item in items:
      total += item.quantity
    return total


class OrderItem(models.Model):
  order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
  product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
  quantity = models.IntegerField(default=0)
  shipping = models.BooleanField(default=False, null=True, blank=True)

  def get_item_total(self):
    total = self.quantity * self.product.price
    return total


class ShippingAddress(models.Model):
  order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
  customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
  first_name = models.CharField(max_length=250, null=True, blank=True)
  last_name = models.CharField(max_length=250, null=True, blank=True)
  email_address = models.EmailField(max_length=250, null=True, blank=True)
  address = models.CharField(max_length=250, null=True, blank=True)
  country = models.CharField(max_length=250, null=True, blank=True)
  zip_code = models.IntegerField(default=0)
  phone = models.IntegerField(default=0)





