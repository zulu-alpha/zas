from django.shortcuts import render


def index(request):
    return HttpResponse("Hello. This is for events.")
