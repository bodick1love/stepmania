from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from user import views as user_view


urlpatterns = [
    path('', include('home.urls')),
    path('catalogue/', include('catalogue.urls')),
    path('user/', include('user.urls')),
    path('register/', user_view.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
