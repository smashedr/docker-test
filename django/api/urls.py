from django.urls import path, include

from . import views

urlpatterns = [
    path('services/', views.ServicesList.as_view(), name='services_list'),
    path('services/create/', views.ServiceCreate.as_view(), name='services_create'),
    path('services/<str:name>/', views.ServiceDetail.as_view(), name='services_get'),
    path('clusters/', views.ClustersList.as_view(), name='clusters_list'),
    path('clusters/<str:cluster>/', views.ClusterDetail.as_view(), name='clusters_get'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
