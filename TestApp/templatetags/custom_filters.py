from django import template
from datetime import datetime
import timeago

register = template.Library()


@register.filter
def timeago_format(value):
    if value:
        return timeago.format(value, datetime.datetime.now())
    return ""
