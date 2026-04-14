from os import name
from platform import version, architecture

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from ..models import TrainModel, Architecture, PerformanceMetric, Tag


class TrainModelTest(TestCase):


    def setUp(self):
        self.data_setup = [(f"test_name_{i}", f"version_{i}") for i in range(0, 3)]
        self.author = get_user_model().objects.create_user(
            username="Test_Researcher",
            password="Test_password",
            specialization="test_specialization_name"
        )
        self.architecture = Architecture.objects.create(
            name="test_architecture",
            description="test_description",
        )

        self.tag = Tag.objects.create(
            name="Test_tag_name"
        )


        for ind, data in enumerate(self.data_setup):
            train_model = TrainModel.objects.create(
                name=data[0],
                version=data[1],
                architecture=self.architecture,
                author=self.author,
            )
            train_model.tags.add(self.tag)
            setattr(self, f"train_model_{ind}", train_model)


    def test_train_model_str(self):
        self.assertEqual(str(self.train_model_0), "Train model name: test_name_0")

    def test_train_model_get_absolute_url(self):
        self.assertEqual(self.train_model_1.get_absolute_url(), reverse("core:train-model-detail", kwargs={"pk":self.train_model_1.pk}))

    def test_unique_train_model(self):
        with self.assertRaises(IntegrityError):
            TrainModel.objects.create(
                name="test_name_0",
                version="version_0",
                architecture=self.architecture,
                author=self.author,
            )

    def test_train_model_multiple_tags(self):
        tag_2 = Tag.objects.create(name="Test_tag_name_2)")
        self.train_model_2.tags.add(tag_2)

        self.assertEqual(self.train_model_2.tags.count(), 2)
        self.assertIn(tag_2, self.train_model_2.tags.all())


class TagTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="tag_name")

    def test_tag_str(self):
        self.assertEqual(str(self.tag), "tag_name")


class ArchitectureTest(TestCase):
    def setUp(self):
        self.architecture = Architecture.objects.create(
            name="test_name",
            description="test_description"
        )

    def test_architecture_str(self):
        self.assertEqual(str(self.architecture), "test_name")


class PerformanceMetricTest(TestCase):
    def setUp(self):
        self.author = get_user_model().objects.create_user(
            username="Test_Researcher_2",
            password="Test_password",
            specialization="AI Research"
        )

        self.architecture = Architecture.objects.create(
            name="test_architecture",
            description="test_description",
        )

        self.train_model = TrainModel.objects.create(
            name="test_train_model_name",
            version="1.1",
            architecture=self.architecture,
            author = self.author
        )
        self.metric = PerformanceMetric.objects.create(
            trained_model = self.train_model,
            accuracy_score=2.2,
            loss_value=0.95
        )

    def test_metric_str(self):
        self.assertEqual(
            str(self.metric),
            "Name test_train_model_name. Accuracy: 2.2."
        )



