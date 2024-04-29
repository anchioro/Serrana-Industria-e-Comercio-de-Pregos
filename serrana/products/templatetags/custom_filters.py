from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def get_full_name_from_username(username):
    try:
        user = User.objects.get(username=username)
        full_name = user.get_full_name()
        return full_name
    except User.DoesNotExist:
        return "Unknown User"
    
@register.filter
def get(d, k):
    return d.get(k, "")

@register.filter(name="get_item")
def get_item(dictionary, key):
    return dictionary.get(key, "")