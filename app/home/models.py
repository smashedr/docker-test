from django.db import models
from django.contrib.auth.models import User


class ToolsManager(models.Manager):
    def get_active(self):
        return self.filter(active=True)

    def get_legacy(self):
        return self.filter(legacy=True)

    def get_active_legacy(self):
        return self.filter(active=True, legacy=True)

    def get_non_legacy(self):
        return self.filter(legacy=False)

    def get_active_non_legacy(self):
        return self.filter(active=True, legacy=False)


class Tools(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(blank=True, null=True)
    git_url = models.URLField(blank=True, null=True)
    legacy = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    maintainer = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ToolsManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.url:
            self.url = self.url.rstrip('/')
        if self.git_url:
            self.git_url = self.git_url.rstrip('/').rstrip('.git')
        super(Tools, self).save()

    class Meta:
        verbose_name = 'Tools'
        verbose_name_plural = 'Tools'
