from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.db.models import Prefetch
from .forms import UserRegisterForm, UserEditForm, ChangePasswordForm
from django.contrib import messages
from .models import Profile
from catalogue.models import Order, Shoes, OrderAndShoes


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

        return self.get(request)  # Re-render the page with the updated context

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