from django import template

register = template.Library()


@register.simple_tag
def if_subscription(user: object, user_request: object):
    for subscriber in user_request.rel_from_set.all():
        if subscriber.user_to == user:
            return True
    return False
