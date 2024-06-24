from django.contrib import admin
from .models import Brand, Category, Shoes, Order, ShoesPhoto, OrderAndShoes


admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Shoes)
admin.site.register(Order)
admin.site.register(ShoesPhoto)
admin.site.register(OrderAndShoes)
