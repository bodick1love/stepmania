from django.db import models


# Create your models here.
class CarouselItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='carousel_items/')

    def __str__(self):
        return self.title