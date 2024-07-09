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

        user_orders = Order.objects.filter(client=current_user)
        user_orders = user_orders.prefetch_related(
            Prefetch('orderandshoes_set__shoes', queryset=Shoes.objects.all())
        )

        orders = {
            order: [order_and_shoes.shoes for order_and_shoes in order.orderandshoes_set.all()] for order in user_orders
        }

        context = {
            'orders': orders,
            'photo': profile.image,
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

    def get(self, request):
        current_user = request.user
        cart, create = Cart.objects.get_or_create(user=current_user)

        shoes = Shoes.objects.filter(cartandshoes__cart=cart).annotate(quantity=F('cartandshoes__quantity'))

        photos = [ShoesPhoto.objects.filter(shoes=item).first() for item in shoes]

        context = {
            'num_items': sum([item.quantity for item in shoes]),
            'total_price': sum([item.price * item.quantity for item in shoes]),
            'cart_items_and_photos': zip(shoes, photos),
        }

        return render(request, self.template_name, context=context)


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
        pass