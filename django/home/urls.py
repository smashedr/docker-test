from django.contrib import admin
from django.templatetags.static import static
from django.urls import path, include
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('favicon\.ico', RedirectView.as_view(url=static('images/favicon.ico')), name='favicon'),
    path('login/', views.show_login, name='login'),
    path('authenticate/', views.do_auth, name='authenticate'),
    path('logout/', views.logout_user, name='logout'),
    path('admin/', admin.site.urls, name='admin'),
    path('api/', include('api.urls')),
]
