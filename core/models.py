from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Researcher(AbstractUser):
    specialization = models.CharField(max_length=255)

    def __str__(self):
        return self.username


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Architecture(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.CharField(max_length=255, verbose_name="Description")
    config = models.JSONField(blank=True, null=True, verbose_name="JSON Configuration")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def __str__(self):
        return self.name


class TrainModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    version = models.CharField(max_length=255)
    architecture = models.ForeignKey(Architecture, on_delete=models.CASCADE, related_name="train_models")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="authored_models")
    tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"Train model name: {self.name}"

    def get_absolute_url(self):
        return reverse("core:train-model-detail", kwargs={"pk": self.pk})


class PerformanceMetric(models.Model):
    trained_model = models.ForeignKey(TrainModel, on_delete=models.CASCADE, related_name="performance_metrics")
    accuracy_score = models.FloatField()
    loss_value = models.FloatField()
    test_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Name {self.trained_model.name}. Accuracy: {self.accuracy_score}."

    def get_absolute_url(self):
        return reverse("core:train-model-detail", kwargs={"pk":self.trained_model.pk})