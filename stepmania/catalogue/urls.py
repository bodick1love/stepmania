from django.urls import path
from . import views


urlpatterns = [
    path('', views.catalogue, name='catalogue'),
    path('<str:model>', views.product, name='model'),
]