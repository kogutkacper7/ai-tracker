from django.urls import path
from .views import ResearcherListView, index_view, TrainModelListView, TrainModelDetailView, ResearcherDetailView, \
    ArchitectureDetailView, TrainModelCreate, ArchitectureListView, contact_view, \
    TrainModelUpdate, TrainModelDelete, PerformanceMetricUpdate, PerformanceMetricDelete, RegisterUser, \
    PerformanceMetricCreate
from django.conf.urls import include

app_name = "core"

urlpatterns = [
    path("", index_view, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("researcher-list/", ResearcherListView.as_view(), name="researcher-list"),
    path("accounts/register/", RegisterUser.as_view(), name="register-user"),
    path("train-model-list/", TrainModelListView.as_view(), name="train-model-list"),
    path("train-model/create/", TrainModelCreate.as_view(), name="train-model-create"),
    path("train-model/detail/<int:pk>/", TrainModelDetailView.as_view(), name="train-model-detail"),
    path("train-model/update/<int:pk>/", TrainModelUpdate.as_view(), name="train-model-update"),
    path("train-model/delete/<int:pk>/", TrainModelDelete.as_view(), name="train-model-delete"),
    path("user-detail/<int:pk>/", ResearcherDetailView.as_view(), name="researcher-detail"),
    path("architecture-detail/<int:pk>/", ArchitectureDetailView.as_view(), name="architecture-detail"),
    path("architecture-list/", ArchitectureListView.as_view(), name="architecture-list"),
    path("contact-us/", contact_view, name="contact-us"),
    path("train-model/metric/create/", PerformanceMetricCreate.as_view(), name="metric-create"),
    path("train-model/metric/update/<int:pk>/", PerformanceMetricUpdate.as_view(), name="metric-update"),
    path("train-model/metric/delete/<int:pk>/", PerformanceMetricDelete.as_view(), name="metric-delete")
]