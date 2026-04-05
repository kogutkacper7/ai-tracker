from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Researcher, TrainModel, Architecture, PerformanceMetric
from .forms import PerformanceMetricForm, ContactUsForm


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


class TrainModelCreate(CreateView):
    model = TrainModel
    template_name = 'core/train_model_create.html'
    fields = ["name", "version", "architecture", "author", "tags"]

    success_url = reverse_lazy("core:train_model-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["train_models"] = TrainModel.objects.all()
        return context


class TrainModelDetailView(DetailView):
    model = TrainModel
    template_name = "core/train_model_detail.html"
    context_object_name = 'train_model'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = PerformanceMetricForm()
        context["form"] = form

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = PerformanceMetricForm(request.POST)

        if form.is_valid():
            new_metric = form.save(commit=False)
            new_metric.trained_model = self.object
            new_metric.save()
            return redirect("core:train-model-detail", pk=self.object.pk)
        context = self.get_context_data(object=self.object)
        context["form"] = form
        return self.render_to_response(context)


class TrainModelDelete(DeleteView):
    model = TrainModel
    success_url = reverse_lazy("core:train_model-list")


class TrainModelUpdate(UpdateView):
    model = TrainModel
    template_name = "core/train_model_update.html"
    fields = ["name", "version"]
    context_object_name = "train_model"


class ResearcherDetailView(DetailView):
    model = Researcher
    template_name = "core/researcher_detail.html"
    context_object_name = "researcher"

class ArchitectureListView(ListView):
    model = Architecture
    template_name = "architecture_list.html"
    context_object_name = "architectures"


class ArchitectureDetailView(DetailView):
    model = Architecture
    template_name = "core/architecture_detail.html"
    context_object_name = "architecture"

def add_performance_metric(request):
    if request.method == "POST":
        form = PerformanceMetricForm(request.POST)

        if form.is_valid():
            new_metric = form.save()
            return redirect("core:train-model-detail", pk=new_metric.trained_model.pk)
    else:
        form = PerformanceMetricForm()

    return render(request, "core/add_metric.html", {"form": form})


def contact_view(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)

        if form.is_valid():
            subject = form.cleaned_data["subject"]
            email = form.cleaned_data["email"]
            content = form.cleaned_data["content"]

            send_mail(
                subject=subject,
                message=f"Wiadomość od: {email}\n\n{content}",
                from_email='system@twojastrona.pl',
                recipient_list=['admin@twojastrona.pl'],
            )
            return redirect("core:index")

    else:
        form = ContactUsForm()
    context = {"form": form}
    return render(request, "core/contact.html", context)


class PerformanceMetricUpdate(UpdateView):
    model = PerformanceMetric
    fields = "__all__"
    template_name = "core/metric_update.html"
    context_object_name = "metric"


class PerformanceMetricDelete(DeleteView):
    model = PerformanceMetric

    def get_success_url(self):
        pk = self.object.trained_model.pk
        return reverse_lazy('core:train-model-detail', kwargs={"pk":pk})
