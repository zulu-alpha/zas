from django.http import HttpResponse


def index(request):
    return HttpResponse("Some poll stuff")
