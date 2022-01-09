from django.templatetags.static import static
from django.urls import reverse
from jinja2 import Environment


def environment(**options):
    """Global environment for Jinja2

    https://docs.djangoproject.com/en/4.0/topics/templates/#module-django.template.backends.django
    """
    # autoescape=True to shut-up bandit, even though it should be set by Django by default.
    env = Environment(autoescape=True, **options)
    env.globals.update({"static": static, "url": reverse})
    return env
