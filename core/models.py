from django.contrib.auth.models import AbstractUser
from django.db import models


class Researcher(AbstractUser):
    specialization = models.CharField(max_length=255)

    def __str__(self):
        return self.username


class Architecture(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.TextField(max_length=255, verbose_name="Description")
    config = models.JSONField(blank=True, null=True, verbose_name="Konfiguracja JSON")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def __str__(self):
        return self.name

class TrainModel(models.Model):
    name = models.CharField(max_length=255)
    version = models.FloatField()
    architecture = models.ForeignKey(Architecture, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class PerformanceMetric(models.Model):
    trained_model = models.ForeignKey(TrainModel, on_delete=models.CASCADE)
    accuracy_score = models.FloatField()
    loss_value = models.FloatField()
    test_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Name {self.trained_model}. Accuracy: {self.accuracy_score}."
