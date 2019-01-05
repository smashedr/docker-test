import ast
import logging
import os
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Services, Clusters
from .serializers import ServiceSerializer
from .serializers import ClusterSerializer

logger = logging.getLogger('app')


class ServicesList(generics.ListCreateAPIView):
    queryset = Services.objects.all()
    serializer_class = ServiceSerializer


class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'name'
    queryset = Services.objects.all()
    serializer_class = ServiceSerializer


class ServiceCreate(APIView):
    # queryset = Services.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['get', 'post']

    def get(self, request, format=None):
        """
        View: /api/services/create/
        """
        # this is only for testing 'get' will not be allowed
        check_access(
            request.user, ast.literal_eval(os.environ['API_CREATE_ALLOWED'])
        )
        return Response('you win')

    def post(self, request):
        """
        View: /api/services/create/
        """
        check_access(
            request.user, ast.literal_eval(os.environ['API_CREATE_ALLOWED'])
        )
        logger.info(request.user.groups.all().values())
        # logic can be added here to reserve a port and return it
        return Response('POST IT!')


class ClustersList(generics.ListCreateAPIView):
    queryset = Clusters.objects.all()
    serializer_class = ClusterSerializer


class ClusterDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'cluster'
    queryset = Clusters.objects.all()
    serializer_class = ClusterSerializer


def check_access(user, groups=None):
    g = groups if isinstance(groups, list) else [groups]
    for group in g:
        if user.groups.filter(name=group).exists():
            return True
    raise PermissionDenied
