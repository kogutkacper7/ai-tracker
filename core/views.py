from django.shortcuts import render
from django.views.generic import ListView
from .models import Researcher


def index_view(request):
    return render(request, "core/index.html")

class ResearcherListView(ListView):
    model = Researcher
    template_name = 'templates/researcher_list.html'
    context_object_name = "researchers"