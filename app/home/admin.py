from django.contrib import admin
from django.utils.html import format_html
from home.models import Tools


@admin.register(Tools)
class ToolsAdmin(admin.ModelAdmin):
    list_display = ('name', 'show_url', 'maintainer', 'active', 'legacy')

    def show_url(self, obj):
        url_string = '<a href="{0}" target="_blank">{0}</a>'
        return format_html(url_string.format(obj.url))
    show_url.short_description = 'URL'
    show_url.admin_order_field = 'url'
