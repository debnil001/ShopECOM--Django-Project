from django.db import models
import datetime


class Category(models.Model):
    name=models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=50)
    price=models.IntegerField(default=0)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    description=models.CharField(max_length=200,default='',null=True,blank=True)
    image=models.ImageField(upload_to='uploads/products/')

    def __str__(self):
        return self.name
class Customer(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=15)
    email=models.EmailField()
    password=models.CharField(max_length=500)

class Orders(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    price=models.IntegerField()
    address=models.CharField(max_length=50,default="",blank=True)
    phone=models.CharField(max_length=50,default="",blank=True)
    datetime=models.DateField(default=datetime.datetime.today)
    status=models.BooleanField(default=False)