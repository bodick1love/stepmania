from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, Brand, Category, Shoes, ShoesPhoto, OrderAndShoes
from django.views import View
from .forms import OrderForm
import json
from django.http import HttpResponse


def catalogue(request):
    shoes = Shoes.objects.all()
    logo = [ShoesPhoto.objects.filter(shoes=shoes[i])[0] for i in range(len(shoes))]

    context = {
        "categories": Category.objects.all(),
        "brands": Brand.objects.all(),
        "shoes": zip(shoes, logo),
        "max_price": max([s.price for s in shoes]),
        "form": OrderForm,
    }

    return render(request, 'catalogue/catalogue.html', context)


def item_page(request, model):
    shoes = get_object_or_404(Shoes, model=model.replace("-", " "))
    shoes_photos = ShoesPhoto.objects.filter(shoes=shoes).all()

    context = {
        'item': shoes,
        'photos': [shoes_photo.image for shoes_photo in shoes_photos],
    }

    return render(request, 'catalogue/item_page.html', context=context)


class OrderView(View):
    def post(self, request):
        data = request.POST.copy()
        shoes = get_object_or_404(Shoes, id=data['item_id'])

        form = OrderForm(data, user=request.user)
        if form.is_valid():
            order = form.save(commit=False)
            order.delivery_price = 5.0
            order.total_price = shoes.price

            order.save()

            connection = OrderAndShoes(order=order, shoes=shoes)
            connection.save()

            return redirect('profile')

        return redirect('catalogue')

    def delete(self, request):
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        order_id = body_data.get('order_id')

        order = get_object_or_404(Order, id=order_id)
        order.delete()

        return HttpResponse(f"Order {order_id} cancelled successfully", content_type="text/plain")