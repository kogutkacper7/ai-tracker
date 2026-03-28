from django.urls import path
from .views import ResearcherListView, index_view

app_name = "core"

urlpatterns = [
    path("", index_view, name="index"),
    path("researcher-list/", ResearcherListView.as_view(), name="researcher-list")
]