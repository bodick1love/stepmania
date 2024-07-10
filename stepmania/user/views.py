from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch, F
from django.contrib import messages
from django.http import HttpResponse
from .forms import UserRegisterForm, UserEditForm, ChangePasswordForm
from .models import Profile, Cart, CartAndShoes
from catalogue.models import Order, Shoes, OrderAndShoes, ShoesPhoto
from catalogue.forms import OrderForm
import json


class ProfileView(LoginRequiredMixin, View):
    template_name = 'user/profile.html'

    def post(self, request):
        current_user = request.user

        if 'user_edit_form' in request.POST:
            user_edit_form = UserEditForm(request.POST, instance=current_user)
            if user_edit_form.is_valid():
                user_edit_form.save()
                messages.success(request, 'Profile updated successfully.')
            else:
                messages.error(request, 'Please correct the error below.')

        elif 'change_password_form' in request.POST:
            change_password_form = ChangePasswordForm(data=request.POST, user=current_user)
            if change_password_form.is_valid():
                change_password_form.save()
                update_session_auth_hash(request, change_password_form.user)  # Important!
                messages.success(request, 'Password changed successfully.')
            else:
                messages.error(request, 'Please correct the error below.')

        return self.get(request)

    def get(self, request):
        current_user = request.user
        profile = current_user.profile

        # Prefetch related shoes for all user orders in one query
        user_orders = Order.objects.filter(client=current_user).prefetch_related(
            Prefetch('orderandshoes_set', queryset=OrderAndShoes.objects.select_related('shoes'))
        )

        # Build orders dictionary with annotated shoes quantities
        orders = {}
        for order in user_orders:
            annotated_shoes = [
                (order_and_shoes.shoes, order_and_shoes.quantity)
                for order_and_shoes in order.orderandshoes_set.all()
            ]
            orders[order] = annotated_shoes

        context = {
            'photo': profile.image,
            'orders': orders,
            'user_edit_form': UserEditForm(instance=current_user),
            'change_password_form': ChangePasswordForm(user=current_user)
        }

        return render(request, 'user/profile.html', context=context)


class RegisterView(View):
    template_name = 'user/register.html'

    def get(self, request):
        form = UserRegisterForm
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile(user=user)
            profile.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account for {username} created successfully!')
            return redirect('login')
        else:
            return render(request, self.template_name, {'form': form})


class CartView(LoginRequiredMixin, View):
    template_name = "user/cart.html"

    def get(self, request, form=OrderForm):
        current_user = request.user
        cart, create = Cart.objects.get_or_create(user=current_user)

        shoes = Shoes.objects.filter(cartandshoes__cart=cart).annotate(quantity=F('cartandshoes__quantity'))

        photos = [ShoesPhoto.objects.filter(shoes=item).first() for item in shoes]

        context = {
            'num_items': sum([item.quantity for item in shoes]),
            'total_price': sum([item.price * item.quantity for item in shoes]),
            'cart_items_and_photos': zip(shoes, photos),
            'form': form,
        }

        return render(request, self.template_name, context=context)

    def post(self, request):
        cart = Cart.objects.filter(user=request.user).first()

        data = request.POST.copy()
        form = OrderForm(data, user=request.user)
        if form.is_valid():
            order = form.save(commit=False)
            order.delivery_price = 5.0
            order.save()

            shoes = Shoes.objects.filter(cartandshoes__cart=cart).annotate(quantity=F('cartandshoes__quantity'))

            for item in shoes:
                connection = OrderAndShoes(order=order, shoes=Shoes.objects.filter(id=item.id).first(), quantity=item.quantity)
                connection.save()

            self.delete(request)

            return HttpResponse("Order place successfully")
        else:
            return self.get(request, form)

    def delete(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        cart.delete()

        return HttpResponse(f"{request.user}'s cart deleted successfully")


class CartAndShoesView(View):
    def post(self, request, shoes_id):
        shoes = get_object_or_404(Shoes, id=shoes_id)
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_and_shoes, created = CartAndShoes.objects.get_or_create(cart=cart, shoes=shoes)
        if not created:
            cart_and_shoes.quantity += 1
        cart_and_shoes.save()

        return HttpResponse(f"Product {shoes.id} was successfully added to cart {cart.id}", content_type="text/plain")

    def delete(self, request, shoes_id):
        cart = get_object_or_404(Cart, user=request.user)

        cart_and_shoes = get_object_or_404(CartAndShoes, cart=cart, shoes=Shoes.objects.filter(id=shoes_id).first())
        cart_and_shoes.delete()

        return HttpResponse(f"Product {shoes_id} was successfully deleted from cart {cart.id}", content_type="text/plain")

    def put(self, request, shoes_id):
        cart_and_shoes = get_object_or_404(CartAndShoes, cart__user=request.user, shoes_id=shoes_id)

        data = json.loads(request.body)
        new_quantity = data.get('quantity')

        if new_quantity == 0:
            return self.delete(request, shoes_id)
        else:
            cart_and_shoes.quantity = new_quantity
            cart_and_shoes.save()

            return HttpResponse(f"Shoes {shoes_id} quantity was successfully updated", content_type="text/plain")