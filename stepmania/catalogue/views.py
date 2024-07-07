from django.shortcuts import render, get_object_or_404
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


def product(request, model):
    shoes = get_object_or_404(Shoes, model=model.replace("-", " "))
    shoes_photos = ShoesPhoto.objects.filter(shoes=shoes).all()

    context = {
        'item': shoes,
        'photos': [shoes_photo.image for shoes_photo in shoes_photos],
    }

    return render(request, 'catalogue/product.html', context=context)