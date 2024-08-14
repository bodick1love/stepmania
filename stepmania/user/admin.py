from django.contrib import admin
from .models import Profile, Cart, CartAndShoes, Feedback


# Register your models here.
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(CartAndShoes)
admin.site.register(Feedback)