from django.contrib.messages import get_messages
from django.templatetags.static import static
from django.urls import reverse
from jinja2 import Environment


def environment(**options):
    """Global environment for Jinja2

    https://docs.djangoproject.com/en/4.0/topics/templates/#module-django.template.backends.django
    """
    env = Environment(**options)  # nosec
    env.globals.update({"static": static, "url": reverse, "get_messages": get_messages})
    return env
