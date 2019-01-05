from django.templatetags.static import static
from django.urls import path
from django.views.generic.base import RedirectView

from home import views

app_name = 'home'

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('about/', views.about, name='about'),
    path('tool/<str:name>', views.tool, name='tool'),
    path('profile/', views.profile, name='profile'),
    path('favicon.ico', RedirectView.as_view(url=static('images/favicon.ico')), name='favicon'),
]
