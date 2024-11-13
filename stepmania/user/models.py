from django.db import models
from django.contrib.auth.models import User
from catalogue.models import Shoes


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='user_images/default.png', upload_to="user_images")

    def __str__(self):
        return f'{self.user.username} profile'


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CartAndShoes(models.Model):
    shoes = models.ForeignKey(Shoes, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'There are {self.quantity} {self.shoes.brand.name} {self.shoes.model} in {self.cart.id} cart'


class Feedback(models.Model):
    # user = models.ForeignKey(User, default=User.objects.get(username='unknown').id, on_delete=models.SET_DEFAULT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f'User {self.user.username} left feedback: {self.text}'