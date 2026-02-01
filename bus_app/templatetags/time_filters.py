from django import template
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now, localtime
from datetime import timedelta

register = template.Library()

@register.filter
def timeago2(value):
    """
    Converts ISO datetime string to human readable "x minutes/hours ago" or "Just now"
    """
    dt = parse_datetime(value)
    if not dt:
        return ""
    
    dt = localtime(dt)
    diff = now() - dt

    if diff < timedelta(minutes=1):
        return "Just now"
    elif diff < timedelta(hours=1):
        minutes = int(diff.total_seconds() // 60)
        return f"{minutes} minutes ago"
    elif diff < timedelta(days=1):
        hours = int(diff.total_seconds() // 3600)
        return f"{hours} hours ago"
    else:
        days = diff.days
        return f"{days} days ago"
