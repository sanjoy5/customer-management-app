from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(
        User, null=True, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    profile_pic = models.ImageField(
        upload_to='profile_imgs/', default="images/icon.png", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)


class Tag(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ('Electronics', 'Electronics'),
        ('Fashion', 'Fashion'),
        ('Grocery', 'Grocery'),

    )
    name = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=100, null=True, choices=CATEGORY)
    image = models.ImageField(upload_to='prod_imgs/', blank=True, null=True)
    desc = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):

    STATUS = (
        ('Pending', "Pending"),
        ('Out for delivery', "Out for delivery"),
        ('Delivered', "Delivered"),
    )

    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=100, null=True, choices=STATUS)

    def __str__(self):
        return f"Order id No : {self.id} - Customer Name : {self.customer} - Product Name : {self.product.name}"
