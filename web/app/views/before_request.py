from copy import deepcopy

from flask import g, request, url_for

from app import app, MENUS

from app.models import Office


@app.before_request
def pass_offices():
    """Passes all the offices off to the templating engine"""
    g.offices = Office.objects.order_by('name')
    g.request_path = request.path

    # Deep copy the menus to avoid evaluating the urls more than once.
    menus = deepcopy(MENUS)
    for menu in menus:
        menu['parent_url'] = eval(menu['parent_url'])
        menu['url'] = eval(menu['url'])

    # Change menu structure to make is easier for use in the templates, because of being
    # grouped in terms of parent url
    g.menus = {}
    # A second dic but only containing a list of sub menu URLs for each parent.
    g.menus_url = {}
    for menu in menus:
        parent_url = menu['parent_url']
        if parent_url not in g.menus:
            g.menus[parent_url] = []
            g.menus_url[parent_url] = []
        g.menus[parent_url].append({'url': menu['url'], 'name': menu['name']})
        g.menus_url[parent_url].append(menu['url'])
