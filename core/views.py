from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Researcher, TrainModel, Architecture, PerformanceMetric, Tag
from .forms import PerformanceMetricForm, ContactUsForm, ResearcherCreationForm


def index_view(request):
    researchers = Researcher.objects.all().count()
    tags = Tag.objects.all().count()
    architectures = Architecture.objects.all().count()
    train_models = TrainModel.objects.all().count()
    performance_metric = PerformanceMetric.objects.all().count()
    context = {
        "total_researchers": researchers,
        "tags": tags,
        "architectures": architectures,
        "train_models": train_models,
        "performance_metric": performance_metric
               }
    return render(request, "core/index.html", context)

class ResearcherListView(ListView):
    model = Researcher
    template_name = 'core/researcher_list.html'
    context_object_name = "researchers"


class TrainModelListView(ListView):
    model = TrainModel
    template_name = 'core/train_model_list.html'
    context_object_name = 'train_models'
    paginate_by = 2


class TrainModelCreate(LoginRequiredMixin, CreateView):
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


class TrainModelDelete(LoginRequiredMixin, DeleteView):
    model = TrainModel
    success_url = reverse_lazy("core:train_model-list")


class TrainModelUpdate(LoginRequiredMixin, UpdateView):
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


class PerformanceMetricUpdate(LoginRequiredMixin, UpdateView):
    model = PerformanceMetric
    fields = "__all__"
    template_name = "core/metric_update.html"
    context_object_name = "metric"


class PerformanceMetricDelete(LoginRequiredMixin, DeleteView):
    model = PerformanceMetric

    def get_success_url(self):
        pk = self.object.trained_model.pk
        return reverse_lazy('core:train-model-detail', kwargs={"pk":pk})


class RegisterUser(CreateView):
    model = Researcher
    form_class = ResearcherCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy('core:login')