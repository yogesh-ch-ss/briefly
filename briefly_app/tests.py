from django.test import TestCase
from django.urls import reverse
from briefly_app.models import BrieflyUser, Category, UserCategory, NewsArticle


# Create your tests here.

class UserViewsTestCases(TestCase):
    def setUp(self):
        self.user = BrieflyUser.objects.create_user(username="testuser", email="test@gmail.com", password="testpassword")
        self.category = Category.objects.create(CategoryName="Technology")
        UserCategory.objects.create(User=self.user, Category=self.category)

    # def test_user_signup(self):

    #     BrieflyUser.objects.all().delete()

    #     url = reverse("briefly:user_signup")
    #     form_data = {
    #         'username': 'testuser',
    #         'password': 'testpassword',
    #         'password_confirmation': 'testpassword',
    #         'country': 'in',
    #         # 'categories': [''],
    #     }
    #     response = self.client.post(reverse('briefly:user_signup'), form_data)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse('briefly:user_login'))

    # def test_user_signup(self):
    #     response = self.client.get(reverse('briefly:user_signup'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'signup.html')

    def test_user_login(self):
        url = reverse('briefly:user_login')
        form_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }

        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 302)  # Should redirect after successful login
        self.assertRedirects(response, reverse('briefly:top_page'))

    def test_user_logout(self):
        self.client.login(username="testuser", password="testpassword")
        url = reverse('briefly:user_logout')
        response = self.client.post(url)
        self.assertRedirects(response, reverse('briefly:top_page'))
