from django import template
from src.authorization.models import CustomUser

register = template.Library()


@register.simple_tag
def get_subscription_in_subscribers(subscriber, user_id):
    user = CustomUser.objects.get(id=user_id)
    for subscribe in user.rel_to_set.all():
        if subscriber == subscribe.user_from:
            return True
    return False
