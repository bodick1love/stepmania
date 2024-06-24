from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Brand(models.Model):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return f'Brand: {self.name};'


class Category(models.Model):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return f'Category: {self.name};'


class Shoes(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    model = models.CharField(max_length=50, null=False)
    price = models.FloatField()
    availability = models.BooleanField()
    description = models.TextField(max_length=300)

    def __str__(self):
        return f'{self.brand}\n {self.category}\n Model: {self.model};\n Price: {self.price}$;\n' \
               f'Availability: {self.availability};\n Description: {self.description};'


class Order(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(default=timezone.now)
    address = models.CharField(max_length=100, null=False)
    payment = models.BooleanField(null=False)
    delivery_price = models.FloatField(null=False)

    def __str__(self):
        return f'{self.client}\n Date: {self.registration_date}\n Address: {self.address}\n' \
               f'Payment: {"YES" if self.payment == True else "NO"}\n Delivery price: {self.delivery_price}'


class OrderAndShoes(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=1)
    shoes = models.ForeignKey(Shoes, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'Shoes: {self.shoes.model} are in order: {self.order.address}'


class ShoesPhoto(models.Model):
    image = models.ImageField(upload_to='shoes_photo/')
    shoes = models.ForeignKey(Shoes, on_delete=models.CASCADE)