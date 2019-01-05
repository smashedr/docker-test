from django.urls import path

from login import views

app_name = 'login'

urlpatterns = [
    path('', views.show_login, name='show'),
    path('auth/', views.do_auth, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
