from flask import g, request

from app import app

from app.models import Office


@app.before_request
def pass_offices():
    """Passes all the offices off to the templating engine"""
    g.offices = Office.objects.order_by('name')
    g.request_path = request.path
