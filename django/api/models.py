from django.db import models


class Services(models.Model):
    name = models.CharField(max_length=255)
    port = models.CharField(max_length=5)
    url = models.CharField(max_length=255)
    env = models.CharField(max_length=255)
    cluster = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Clusters(models.Model):
    cluster = models.CharField(max_length=255)
    services = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cluster
