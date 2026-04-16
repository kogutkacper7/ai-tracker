from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Researcher

from .models import PerformanceMetric

class PerformanceMetricForm(forms.ModelForm):
    class Meta:
        model = PerformanceMetric
        fields = ["accuracy_score", "loss_value"]


class ContactUsForm(forms.Form):
    subject = forms.CharField(max_length=30)
    email = forms.EmailField()
    content = forms.CharField(max_length=255)


class ResearcherCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Researcher
        fields = UserCreationForm.Meta.fields + ("specialization",)

