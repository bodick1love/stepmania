from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='user_images/default.png', upload_to="user_images")

    def __str__(self):
        return f'{self.user.username} profile'