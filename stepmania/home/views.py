from django.db.models import Count
from django.shortcuts import render
from .models import CarouselItem
from catalogue.models import Shoes, OrderAndShoes, ShoesPhoto


def home(request):
    carousel_items = CarouselItem.objects.all()

    # Annotate each shoe with the number of orders it has
    shoes_with_order_count = Shoes.objects.annotate(order_count=Count('orderandshoes'))

    shoes_with_order_count = shoes_with_order_count.filter(availability=True)

    # Order the queryset by order count in descending order and get the top 4 shoes
    top_4_shoes = shoes_with_order_count.order_by('-order_count', '-price')[:4]

    logos = [ShoesPhoto.objects.filter(shoes=s)[0] for s in top_4_shoes]

    bestsellers = zip(top_4_shoes, logos)

    context = {
        'carousel_items': carousel_items,
        'bestsellers': bestsellers,
    }

    return render(request, 'home/home.html', context=context)
