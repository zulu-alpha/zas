from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class ProfileView(TemplateView):
    template_name = "profiles/profile.j2"


class HomeView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "profiles/home.j2"

    def get(self, request):
        return Response()
