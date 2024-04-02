from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    return render(request, 'user/profile.html')


class RegisterView(View):
    template_name = 'user/register.html'

    def get(self, request):
        form = RegisterForm
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request, f'Account for {username} created successfully! ')
            return redirect('home')