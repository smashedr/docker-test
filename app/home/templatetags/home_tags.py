from django import template
from base64 import b64encode

register = template.Library()


#  Filters

@register.filter(name='b64_image', is_safe=True)
def b64_image(value, image_type):
    try:
        return 'data:{};base64,{}'.format(image_type, b64encode(value).decode())
    except Exception:
        return None
