from rest_framework import serializers
from . import models


class ServiceSerializer(serializers.ModelSerializer):
    port = serializers.CharField(required=False, read_only=True, max_length=5)

    class Meta:
        many = True
        model = models.Services
        fields = ('id', 'name', 'port', 'url', 'env', 'cluster', 'created_at', 'updated_at')


class ClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Clusters
        fields = ('id', 'cluster', 'services', 'created_at', 'updated_at',)
