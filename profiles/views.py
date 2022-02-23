from django.views.generic import TemplateView


class ProfileView(TemplateView):
    template_name = "profiles/profile.j2"


class HomeView(TemplateView):
    template_name = "profiles/home.j2"
