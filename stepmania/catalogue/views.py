from django.shortcuts import render
from .models import Brand, Category, Shoes, ShoesPhoto


def catalogue(request):
    shoes = Shoes.objects.all()
    logo = [ShoesPhoto.objects.filter(shoes=shoes[i])[0] for i in range(len(shoes))]
    context = {
                "categories": Category.objects.all(),
                "brands": Brand.objects.all(),
                "shoes_logo": zip(shoes, logo),
                "max_price": max([s.price for s in shoes]),
    }
    return render(request, 'catalogue/catalogue.html', context)