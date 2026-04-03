from django.urls import path
from .views import ResearcherListView, index_view, TrainModelListView, TrainModelDetailView, ResearcherDetailView, ArchitectureDetailView
from django.conf.urls import include
app_name = "core"

urlpatterns = [
    path("", index_view, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("researcher-list/", ResearcherListView.as_view(), name="researcher-list"),
    path("train_model-list/", TrainModelListView.as_view(), name="train_model-list"),
    path("train_model-detail/<int:pk>/", TrainModelDetailView.as_view(), name="train-model-detail"),
    path("user-detail/<int:pk>", ResearcherDetailView.as_view(), name="researcher-detail"),
    path("archtecture-detail/<int:pk>", ArchitectureDetailView.as_view(), name="archtecture-detail")
]