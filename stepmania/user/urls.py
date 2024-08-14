from django.urls import path
from . import views


urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart-and-shoes/<int:shoes_id>/', views.CartAndShoesView.as_view(), name='cart-and-shoes'),
    path('feedback/', views.FeedbackView.as_view(), name='feedback')
]