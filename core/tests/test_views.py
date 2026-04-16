from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import Architecture, Tag, TrainModel, PerformanceMetric


class ResearcherViewTest(TestCase):

    def setUp(self):
        self.author = get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
            specialization="test_specialization",
        )

        self.client.login(username="test_username", password="test_password")

    def test_signup_view_status_code(self):
        url = reverse("core:register-user")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")

    def test_researcher_detail_view(self):
        url = reverse("core:researcher-detail", kwargs={"pk": self.author.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_specialization")
        self.assertContains(response, "test_username")

    def test_login_mechanism_for_views(self):

        is_logged_in = self.client.login(
            username="test_username", password="test_password"
        )
        self.assertTrue(is_logged_in)

    def test_search_bar_researcher_list(self):
        self.other_author = get_user_model().objects.create_user(
            username="completely_different_user",
            password="test_other_password",
            specialization="test_specialization",
        )
        url = reverse("core:researcher-list")
        response = self.client.get(url, {"search": "test_username"})

        self.assertContains(response, "test_username")
        self.assertNotContains(response, "completely_different_user")

    def test_no_results_search_bar_researcher_list(self):
        url = reverse("core:researcher-list")
        response = self.client.get(url, {"search": "DoesntExistUser"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["researchers"]), 0)

    def test_pagination(self):

        for i in range(0, 10):
            get_user_model().objects.create(
                username=f"Test_{i}",
                password=f"Password_{i}",
                specialization=f"specialization_{i}",
            )

        url = reverse("core:researcher-list")
        response = self.client.get(url)
        response_1 = self.client.get(url, {"page": 2})

        self.assertEqual(len(response.context["researchers"]), 5)
        self.assertEqual(len(response_1.context["researchers"]), 5)


class TrainModelViewTest(TestCase):
    def setUp(self):
        self.author = get_user_model().objects.create_user(
            username="Test_Researcher",
            password="Test_password",
            specialization="test_specialization_name",
        )
        self.architecture = Architecture.objects.create(
            name="test_architecture",
            description="test_description",
        )

        self.tag = Tag.objects.create(name="Test_tag_name")

        self.train_model = TrainModel.objects.create(
            name="test_train_model",
            version="1.1",
            architecture=self.architecture,
            author=self.author,
        )

        self.train_model.tags.add(self.tag)

    def test_train_model_detail_test(self):
        url = reverse("core:train-model-detail", kwargs={"pk": self.train_model.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1.1")
        self.assertContains(response, "test_train_model")

    def test_search_bar_train_model_list(self):
        self.other_train_model = TrainModel.objects.create(
            name="completely_different_model",
            version="1.2",
            architecture=self.architecture,
            author=self.author,
        )

        url = reverse("core:train-model-list")
        response = self.client.get(url, {"search": "test_train_model"})

        self.assertContains(response, "test_train_model")
        self.assertNotContains(response, "completely_different_model")

    def test_no_results_search_bar_train_models(self):
        url = reverse("core:train-model-list")
        response = self.client.get(url, {"search": "DoesntExistUser"})

        self.assertEqual(len(response.context["train_models"]), 0)

    def test_pagination(self):

        for i in range(0, 9):
            TrainModel.objects.create(
                name=f"train_model_{i}",
                version=f"1.{i}",
                architecture=self.architecture,
                author=self.author,
            )

        url = reverse("core:train-model-list")
        response = self.client.get(url)
        response_1 = self.client.get(url, {"page": 2})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["train_models"]), 5)
        self.assertEqual(len(response_1.context["train_models"]), 5)

    def test_create_train_model(self):
        self.client.login(username="Test_Researcher", password="Test_password")

        self.assertEqual(TrainModel.objects.count(), 1)

        url = reverse("core:train-model-create")
        response = self.client.post(
            url,
            {
                "name": "New_created_name",
                "version": "2.1",
                "architecture": self.architecture.pk,
                "author": self.author.pk,
                "tags": [self.tag.pk],
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(TrainModel.objects.count(), 2)

    def test_update_train_model(self):
        self.client.login(username="Test_Researcher", password="Test_password")

        url = reverse("core:train-model-update", kwargs={"pk": self.train_model.pk})
        response = self.client.post(url, {"name": "New_update_name", "version": "2.1"})

        self.assertEqual(response.status_code, 302)
        self.train_model.refresh_from_db()

        self.assertEqual(self.train_model.name, "New_update_name")
        self.assertEqual(self.train_model.version, "2.1")

    def test_delete_train_models(self):
        self.client.login(username="Test_Researcher", password="Test_password")

        self.assertEqual(TrainModel.objects.count(), 1)

        url = reverse("core:train-model-delete", kwargs={"pk": self.train_model.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(TrainModel.objects.count(), 0)

    def test_delete_require_login(self):
        self.client.logout()

        url = reverse("core:train-model-delete", kwargs={"pk": self.train_model.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        self.assertEqual(TrainModel.objects.count(), 1)


class ArchitectureViewTest(TestCase):
    def setUp(self):
        self.architecture = Architecture.objects.create(
            name="test_architecture",
            description="test_description",
        )

    def test_architecture_detail(self):
        self.author = get_user_model().objects.create_user(
            username="Test_Researcher",
            password="Test_password",
            specialization="test_specialization_name",
        )

        for i in range(0, 4):
            TrainModel.objects.create(
                name=f"train_model_{i}",
                version=f"1.{i}",
                architecture=self.architecture,
                author=self.author,
            )

        url = reverse("core:architecture-detail", kwargs={"pk": self.architecture.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_architecture")
        self.assertEqual(self.architecture.train_models.count(), 4)

    def test_search_bar_architectures(self):
        self.other_architecture = Architecture.objects.create(
            name="example_name",
            description="other_test_description",
        )

        url = reverse("core:architecture-list")
        response = self.client.get(url, {"search": "test_architecture"})

        self.assertContains(response, "test_architecture")
        self.assertNotContains(response, "example_name")

    def test_no_results_search_bar_architecture(self):
        url = reverse("core:architecture-list")
        response = self.client.get(url, {"search": "DoesntExistArchitecture"})

        self.assertEqual(len(response.context["architectures"]), 0)

    def test_pagination_architecture(self):
        for i in range(0, 9):
            Architecture.objects.create(
                name=f"test_architecture_{i}", description=f"test_description_{i}"
            )

        url = reverse("core:architecture-list")
        response = self.client.get(url)
        response_1 = self.client.get(url, {"page": 2})

        self.assertEqual(len(response.context["architectures"]), 5)
        self.assertEqual(len(response_1.context["architectures"]), 5)


class PerformanceViewTest(TestCase):
    def setUp(self):
        self.author = get_user_model().objects.create_user(
            username="Test_Researcher",
            password="Test_password",
            specialization="test_specialization_name",
        )
        self.architecture = Architecture.objects.create(
            name="test_architecture",
            description="test_description",
        )

        self.tag = Tag.objects.create(name="Test_tag_name")

        self.train_model = TrainModel.objects.create(
            name="test_train_model",
            version="1.1",
            architecture=self.architecture,
            author=self.author,
        )

        self.train_model.tags.add(self.tag)

        self.metric = PerformanceMetric.objects.create(
            trained_model=self.train_model, accuracy_score=2.3, loss_value=1.6
        )

    def test_metric_str(self):
        self.assertEqual(str(self.metric), f"Name test_train_model. Accuracy: 2.3.")

    def test_metric_detail(self):
        url = reverse("core:train-model-detail", kwargs={"pk": self.train_model.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "2.3")
        self.assertContains(response, "1.6")

    def test_create_metric(self):
        self.client.login(username="Test_Researcher", password="Test_password")

        self.assertEqual(PerformanceMetric.objects.count(), 1)

        base_url = reverse("core:metric-create")
        url = f"{base_url}?train_model={self.train_model.pk}"
        response = self.client.post(url, {"accuracy_score": 1.9, "loss_value": 1.4})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(PerformanceMetric.objects.count(), 2)

    def test_update_metric(self):
        self.client.login(username="Test_Researcher", password="Test_password")

        url = reverse("core:metric-update", kwargs={"pk": self.metric.pk})
        response = self.client.post(url, {"accuracy_score": 3.3, "loss_value": 4.4})

        self.assertEqual(response.status_code, 302)
        self.metric.refresh_from_db()

        self.assertEqual(self.metric.accuracy_score, 3.3)
        self.assertEqual(self.metric.loss_value, 4.4)

    def test_delete_metric(self):
        self.client.login(username="Test_Researcher", password="Test_password")

        self.assertEqual(PerformanceMetric.objects.count(), 1)

        url = reverse("core:metric-delete", kwargs={"pk": self.metric.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(PerformanceMetric.objects.count(), 0)


class ContactTest(TestCase):

    def setUp(self):
        self.author = get_user_model().objects.create_user(
            username="Test_user_name",
            password="Password",
            specialization="test_specialization",
        )

        self.client.login(username="Test_user_name", password="Password")

    def test_contact_page_status_code(self):
        url = reverse("core:contact-us")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/contact.html")

    def test_contact_form_invalid_data(self):
        url = reverse("core:contact-us")
        response = self.client.post(url, data={})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)

    def test_contact_form_valid_data(self):
        url = reverse("core:contact-us")
        response = self.client.post(
            url,
            data={
                "subject": "Test_subject",
                "email": "kacper@test.com",
                "content": "This test message.",
            },
        )

        self.assertEqual(response.status_code, 302)


class IndexViewTest(TestCase):
    def setUp(self):
        self.author = get_user_model().objects.create_user(
            username="Test_Researcher",
            password="Test_password",
            specialization="test_specialization_name",
        )
        self.architecture = Architecture.objects.create(
            name="test_architecture",
            description="test_description",
        )

        self.tag = Tag.objects.create(name="Test_tag_name")

        for i in range(0, 5):

            train_model = TrainModel.objects.create(
                name=f"test_train_model_{i}",
                version=f"1.{i}",
                architecture=self.architecture,
                author=self.author,
            )

            train_model.tags.add(self.tag)
            setattr(self, f"train_model{i}", train_model)

    def test_index_status_code_and_templates(self):
        url = reverse("core:index")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/index.html")

    def test_index_context_statistics(self):
        url = reverse("core:index")
        response = self.client.get(url)

        self.assertEqual(response.context["total_researchers"], 1)
        self.assertEqual(response.context["tags"], 1)
        self.assertEqual(response.context["architectures"], 1)
        self.assertEqual(response.context["train_models"], 5)
        self.assertEqual(response.context["performance_metric"], 0)

    def test_last_added_models(self):
        url = reverse("core:index")
        response = self.client.get(url)

        self.assertEqual(len(response.context["last_added_models"]), 3)

    def test_session_num_visits(self):
        url = reverse("core:index")

        response = self.client.get(url)
        self.assertEqual(response.context["num_visits"], 1)

        response_1 = self.client.get(url)
        self.assertEqual(response_1.context["num_visits"], 2)
