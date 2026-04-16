from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Researcher, TrainModel, Architecture, PerformanceMetric, Tag
from .forms import PerformanceMetricForm, ContactUsForm, ResearcherCreationForm

def index_view(request):
    researchers = Researcher.objects.all().count()
    tags = Tag.objects.all().count()
    architectures = Architecture.objects.all().count()
    train_models = TrainModel.objects.all().count()
    performance_metric = PerformanceMetric.objects.all().count()

    last_added_models = TrainModel.objects.order_by("-id")[:3]

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "total_researchers": researchers,
        "tags": tags,
        "architectures": architectures,
        "train_models": train_models,
        "performance_metric": performance_metric,
        "num_visits": num_visits + 1,
        "last_added_models": last_added_models
               }
    return render(request, "core/index.html", context)

class ResearcherListView(ListView):
    model = Researcher
    template_name = 'core/researcher_list.html'
    context_object_name = "researchers"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()

        search_value = self.request.GET.get("search")

        if search_value:
            queryset = queryset.filter(username__icontains=search_value)
            return queryset

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["search_value"] = self.request.GET.get('search', '')

        return context

class TrainModelListView(ListView):
    model = TrainModel
    template_name = 'core/train_model_list.html'
    context_object_name = 'train_models'
    paginate_by = 5

    def get_queryset(self):
        queryset = TrainModel.objects.select_related("architecture", "author").prefetch_related("tags")

        search_value = self.request.GET.get("search")

        if search_value:
            queryset = queryset.filter(name__icontains=search_value)

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['search_value'] = self.request.GET.get('search', '')
        return context


class TrainModelCreate(LoginRequiredMixin, CreateView):
    model = TrainModel
    template_name = 'core/train_model_create.html'
    fields = ["name", "version", "architecture", "tags"]

    success_url = reverse_lazy("core:train-model-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["train_models"] = TrainModel.objects.all()
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


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

    def get_object(self, queryset=None):
        return (
            TrainModel.objects
            .prefetch_related("performance_metrics")
            .get(pk=self.kwargs["pk"])
        )


class TrainModelDelete(LoginRequiredMixin, DeleteView):
    model = TrainModel
    success_url = reverse_lazy("core:train-model-list")
    context_object_name = "train_model"


class TrainModelUpdate(LoginRequiredMixin, UpdateView):
    model = TrainModel
    template_name = "core/train_model_update.html"
    fields = ["name", "version"]
    context_object_name = "train_model"


class ResearcherDetailView(DetailView):
    model = Researcher
    template_name = "core/researcher_detail.html"
    context_object_name = "researcher"

    def get_object(self, queryset=None):
        return (
            Researcher.objects
            .prefetch_related("authored_models__architecture")
            .get(pk=self.kwargs["pk"])
        )

class ArchitectureListView(ListView):
    model = Architecture
    template_name = "core/architecture_list.html"
    context_object_name = "architectures"
    paginate_by = 5

    def get_queryset(self):

        queryset = super().get_queryset()

        search_value = self.request.GET.get("search")

        if search_value:
            queryset = queryset.filter(name__icontains=search_value)
        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data()
        context["search_value"] = self.request.GET.get("search", '')
        return context

class ArchitectureDetailView(DetailView):
    model = Architecture
    template_name = "core/architecture_detail.html"
    context_object_name = "architecture"

    def get_object(self, queryset=None):
        return (
            Architecture.objects
            .prefetch_related("train_models__author")
            .get(pk=self.kwargs["pk"])
        )

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


class PerformanceMetricCreate(LoginRequiredMixin, CreateView):
    model = PerformanceMetric
    form_class = PerformanceMetricForm
    template_name = "core/metric_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_id = self.request.GET.get("train_model")

        if model_id:
            context["train_model"] = get_object_or_404(TrainModel, pk=model_id)

        return context

    def get_initial(self):
        initial = super().get_initial()
        model_id = self.request.GET.get("train_model")

        if model_id:
            initial["trained_model"] = model_id

        return initial

    def form_valid(self, form):
        model_id = self.request.GET.get('train_model')
        if model_id:
            form.instance.trained_model_id = model_id
        return super().form_valid(form)

    def get_success_url(self):
        return  reverse_lazy('core:train-model-detail', kwargs={"pk": self.object.trained_model.pk })

class PerformanceMetricUpdate(LoginRequiredMixin, UpdateView):
    model = PerformanceMetric
    fields = ["accuracy_score", "loss_value"]
    template_name = "core/metric_update.html"
    context_object_name = "metric"


class PerformanceMetricDelete(LoginRequiredMixin, DeleteView):
    model = PerformanceMetric
    context_object_name = "metric"

    def get_success_url(self):
        pk = self.object.trained_model.pk
        return reverse_lazy('core:train-model-detail', kwargs={"pk":pk})



class RegisterUser(CreateView):
    model = Researcher
    form_class = ResearcherCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy('core:login')