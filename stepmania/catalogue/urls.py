from django.urls import path
from . import views


urlpatterns = [
    path('', views.catalogue, name='catalogue'),
    path('order', views.OrderView.as_view(), name="order"),
    path('<str:model>', views.shoes, name='shoes'),
]