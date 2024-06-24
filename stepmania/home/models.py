from django.db import models

<<<<<<< HEAD

# Create your models here.
class CarouselItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='carousel_items/')

    def __str__(self):
        return self.title
=======
# Create your models here.
>>>>>>> e48776e10b74c39156b7ccd96cae1124b8884d49
