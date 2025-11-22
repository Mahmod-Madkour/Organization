from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Login / Logout
    path('login/', auth_views.LoginView.as_view(template_name='admin/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # App
    path('', include('Quran.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]
