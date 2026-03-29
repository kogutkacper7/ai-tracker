from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Researcher, TrainModel, Architecture


def index_view(request):
    return render(request, "core/index.html")

class ResearcherListView(ListView):
    model = Researcher
    template_name = 'core/researcher_list.html'
    context_object_name = "researchers"


class TrainModelListView(ListView):
    model = TrainModel
    template_name = 'core/train_model_list.html'
    context_object_name = 'train_models'


class TrainModelDetailView(DetailView):
    model = TrainModel
    template_name = "core/train_model_detail.html"
    context_object_name = 'train_model'


class ResearcherDetailView(DetailView):
    model = Researcher
    template_name = "core/researcher_detail.html"
    context_object_name = "researcher"


class ArchitectureDetailView(DetailView):
    model = Architecture
    template_name = "core/architecture_detail.html"
    context_object_name = "architecture"
