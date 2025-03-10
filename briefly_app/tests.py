from briefly_app.models import BrieflyUser, Category, UserCategory, NewsArticle, SavedNews, COUNTRY_CHOICES, CATEGORY_CHOICES, ViewedNews
from django.core.exceptions import ValidationError
from django.db import IntegrityError

import unittest
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from briefly_app.forms import BrieflyUserLoginForm, BrieflyUserProfileForm, BrieflyUserSignupForm
from django.contrib.auth import authenticate, login
from django.urls import reverse

# Create your tests here.
class TestBrieflyUser(TestCase):
    def setUp(self):
        self.user = BrieflyUser.objects.create(username='testuser', password='testpassword', country='in')
    
    def test_str(self):
        self.assertEqual(str(self.user), 'testuser')

    # This will trigger the validation error for invalid country code.
    def test_invalid_country(self):
        with self.assertRaises(ValidationError):
            invalid_user = BrieflyUser(username='invaliduser', password='testpassword', country='xx')
            invalid_user.full_clean() 
    
    # This will NOT trigger the validation error as 'us' is a valid country code.
    def test_valid_country(self):
        valid_user = BrieflyUser(username='validuser', password='testpassword', country='us')
        valid_user.full_clean()
        valid_user.save()
        self.assertEqual(valid_user.country, 'us')
    

class TestCategory(TestCase):
    def setUp(self):
        self.category = Category.objects.create(CategoryName='business')
    
    # This will trigger the validation error for invalid category name.
    def test_invalid_category(self):
        with self.assertRaises(ValidationError):
            invalid_category = Category.objects.create(CategoryName='invalidcategory')
            invalid_category.full_clean() 
    
    # Try to create Business instead of business -> This will trigger the validation error for case-sensitive category name.
    def test_case_sensitive_category(self):
        with self.assertRaises(ValidationError):
            case_sensitive_category = Category(CategoryName='Business')
            case_sensitive_category.full_clean()

    # Try to create a duplicate category. -> This will trigger the validation error.
    def test_valid_category(self):
        with self.assertRaises(ValidationError):
            duplicate_category = Category(CategoryName='business')
            duplicate_category.full_clean()


class TestUserCategory(TestCase):
    def setUp(self):
        self.user = BrieflyUser.objects.create(username='testuser', password='testpassword', country='in')
        self.category = Category.objects.create(CategoryName='business')
        try:
            self.user_category = UserCategory.objects.create(User=self.user, Category=self.category)
        except IntegrityError:
            self.user_category = UserCategory.objects.get(User=self.user, Category=self.category)
    
    def test_str(self):
        self.assertEqual(str(self.user_category), 'testuser - business')
    
    # Try to create a duplicate UserCategory. -> This will trigger the validation error.
    def test_duplicate_user_category(self):
        with self.assertRaises(IntegrityError):
            duplicate_user_category = UserCategory(User=self.user, Category=self.category)
            duplicate_user_category.save()
    
    # Try to create a UserCategory with a deleted user. -> This will trigger the validation error.
    def test_deleted_user(self):
        self.user.delete()
        with self.assertRaises(ValueError):
            deleted_user_category = UserCategory(User=self.user, Category=self.category)
            deleted_user_category.save()

class TestNewsArticle(TestCase):
    def setUp(self):
        self.category = Category.objects.create(CategoryName='technology')
        self.article = NewsArticle.objects.create(
            Title='Tech News',
            Content='Latest in tech.',
            Source='TechSource',
            Category=self.category
        )

    def test_str(self):
        self.assertEqual(str(self.article), 'Tech News')

    def test_invalid_category(self):
        with self.assertRaises(ValidationError):
            invalid_article = NewsArticle(
                Title='Invalid News',
                Content='Invalid content.',
                Source='InvalidSource',
                Category=None
            )
            invalid_article.full_clean()

    def test_duplicate_article(self):
        with self.assertRaises(ValidationError):
            duplicate_article = NewsArticle.objects.create(
                Title='Tech News',
                Content='Latest in tech.',
                Source='TechSource',
                Category=self.category
            )
            duplicate_article.full_clean()

class TestViewedNews(TestCase):
    def setUp(self):
        self.user = BrieflyUser.objects.create(username='testuser', password='testpassword', country='us')
        self.category = Category.objects.create(CategoryName='technology')
        self.article = NewsArticle.objects.create(
            Title='Tech News',
            Content='Latest in tech.',
            Source='TechSource',
            Category=self.category
        )
        self.viewed_news = ViewedNews.objects.create(User=self.user, News=self.article)

    def test_str(self):
        self.assertEqual(str(self.viewed_news), 'testuser Tech News')

    def test_duplicate_viewed_news(self):
        with self.assertRaises(ValidationError):
            duplicate_viewed_news = ViewedNews.objects.create(User=self.user, News=self.article)
            duplicate_viewed_news.full_clean()

class TestSavedNews(TestCase):
    def setUp(self):
        self.user = BrieflyUser.objects.create(username='testuser', password='testpassword', country='us')
        self.category = Category.objects.create(CategoryName='technology')
        self.article = NewsArticle.objects.create(
            Title='Tech News',
            Content='Latest in tech.',
            Source='TechSource',
            Category=self.category
        )
        self.saved_news = SavedNews.objects.create(User=self.user, News=self.article)

    def test_str(self):
        self.assertEqual(str(self.saved_news), 'testuser Tech News')

    def test_duplicate_saved_news(self):
        with self.assertRaises(ValidationError):
            duplicate_saved_news = SavedNews.objects.create(User=self.user, News=self.article)
            duplicate_saved_news.full_clean()

# test case for BrieflyUserSignupForm
class TestBrieflyUserSignupForm(TestCase):
    def setUp(self):
        self.valid_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'password_confirmation': 'testpassword',
            'country': 'us',
            'categories': ['business', 'technology']
        }

        self.invalid_data = self.valid_data.copy()
        self.invalid_data['password_confirmation'] = 'wrongpassword'
        self.invalid_data['email'] = 'invalidemail@example.com'

    def test_valid_form(self):
        form = BrieflyUserSignupForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_password_mismatch(self):
        form = BrieflyUserSignupForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password_confirmation', form.errors)

    def test_save_user(self):
        form = BrieflyUserSignupForm(data=self.valid_data)
        if form.is_valid():
            user = form.save()
            self.assertEqual(user.username, 'testuser')
            self.assertTrue(user.check_password('testpassword'))
            self.assertEqual(user.country, 'us')
            self.assertEqual(UserCategory.objects.filter(User=user).count(), 2)

    def test_invalid_country(self):
        invalid_data = self.valid_data.copy()
        invalid_data['country'] = 'xx'
        form = BrieflyUserSignupForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('country', form.errors)

    def test_zero_country(self):
        invalid_data = self.valid_data.copy()
        invalid_data['country'] = ''
        form = BrieflyUserSignupForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('country', form.errors)
    
    def test_zero_categorychoice(self):
        invalid_data = self.valid_data.copy()
        invalid_data['categories'] = []
        form = BrieflyUserSignupForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('categories', form.errors)

    def test_invalid_email(self):
        form = BrieflyUserSignupForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())

# test case for BrieflyUserLoginForm
class TestBrieflyUserLoginForm(TestCase):
    def setUp(self):
        self.user = BrieflyUser.objects.create(username='testuser', country='us')
        self.user.set_password('testpassword')
        self.user.save()
        self.valid_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        self.invalid_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }

    def test_invalid_login_form(self):
        form = BrieflyUserLoginForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())

    def test_authenticate_valid_user(self):
        form = BrieflyUserLoginForm(data=self.valid_data)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            self.assertIsNotNone(user)
            self.assertEqual(user.username, 'testuser')

    def test_authenticate_invalid_user(self):
        form = BrieflyUserLoginForm(data=self.invalid_data)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            self.assertIsNone(user)

# test case for BrieflyUserProfileForm
class TestBrieflyUserProfileForm(TestCase):
    def setUp(self):
        self.user = BrieflyUser.objects.create(username='testuser', email='testuser@example.com', country='us')
        self.category1 = Category.objects.create(CategoryName='business')
        self.category2 = Category.objects.create(CategoryName='technology')
        UserCategory.objects.create(User=self.user, Category=self.category1)
        UserCategory.objects.create(User=self.user, Category=self.category2)
        self.valid_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'country': 'us',
            'categories': ['business', 'technology']
        }
        self.invalid_data = self.valid_data.copy()
        self.invalid_data['categories'] = []

    def test_invalid_form_no_categories(self):
        form = BrieflyUserProfileForm(data=self.invalid_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('categories', form.errors)

    def test_initial_data(self):
        form = BrieflyUserProfileForm(instance=self.user)
        self.assertEqual(form.fields['username'].initial, 'testuser')
        self.assertEqual(form.fields['email'].initial, 'testuser@example.com')
        self.assertEqual(form.fields['country'].initial, 'us')
        self.assertListEqual(form.fields['categories'].initial, ['business', 'technology'])
        
# This test case is for the NewsArticle model.
class UserViewsTestCases(TestCase):
    def setUp(self):
        self.user = BrieflyUser.objects.create_user(username="testuser", email="test@email.com", password="testpassword")
        self.category = Category.objects.create(CategoryName="Technology")

        self.client.login(username='testuser', password='testpassword')
        
        UserCategory.objects.create(User=self.user, Category=self.category)

        NewsArticle.objects.create(
            Title="Tech News",
            Content="Latest in tech.",
            Source="TechSource",
            Category=self.category
        )

    # @unittest.skip("Skipping this test (test_user_signup) temporarily")
    def test_user_signup(self):

        self.client.logout()

        url = reverse("briefly:user_signup")
        form_data = {
            'username': 'newuser',
            'password': 'newpassword',
            'password_confirmation': 'newpassword',
            'country': 'gb',
            'categories': ['technology'],
        }
        
        response = self.client.post(reverse('briefly:user_signup'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('briefly:user_login'))

        print("\n---\nSUCCESS: test_user_signup \n---")


    def test_user_signup(self):
        self.client.logout()
        response = self.client.get(reverse('briefly:user_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_user_login(self):
        self.client.logout()
        url = reverse('briefly:user_login')
        form_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, form_data)
        print(response.status_code)
        self.assertEqual(response.status_code, 302)  # 302 - redirect after successful login
        self.assertRedirects(response, reverse('briefly:user_news'))
        print("\n---\nSUCCESS: test_user_login \n---")

    def test_user_logout(self):
        self.client.login(username="testuser", password="testpassword")
        url = reverse('briefly:user_logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('briefly:top_page'))

        print("\n---\nSUCCESS: test_user_logout \n---")

    def test_user_delete_account(self):
        self.client.login(username="testuser", password="testpassword")
        url = reverse('briefly:user_delete_account')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('briefly:top_page'))
        print("\n---\nSUCCESS: test_user_delete_account \n---")

    # user_profile_setting
    def test_user_profile_setting(self):
        self.client.login(username="testuser", password="testpassword")
        url = reverse('briefly:user_profile_setting')
        form_data = {
            'username': 'testuser',
            'email': '',
            'country': 'us',
            'categories': ['technology']
        }
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('briefly:user_news'))
        print("\n---\nSUCCESS: test_user_profile_setting \n---")


    def test_get_user_news(self):
        self.client.login(username="testuser", password="testpassword")
        url = reverse('briefly:user_news')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'headlines.html')
        print("\n---\nSUCCESS: test_get_user_news \n---")

    # test save_article
    def test_save_article(self):
        self.client.login(username="testuser", password="testpassword")
        save_article = NewsArticle.objects.create(
            Title="Sample News",
            Content="Saple content",
            Source="SampleSource",
            Category=self.category
        )
        url = reverse('briefly:save_article')
        form_data = {
            'article_id': save_article.NewsID,
            'user_id': self.user.id
        }
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 204)  # No Content
        self.assertTrue(SavedNews.objects.filter(User=self.user, News=save_article).exists())
        print("\n---\nSUCCESS: test_save_article \n---")

    def test_saved_articles(self):
        self.client.login(username="testuser", password="testpassword")
        saved_article = NewsArticle.objects.create(
            Title="Sample News",
            Content="Sample content",
            Source="SampleSource",
            Category=self.category
        )
        SavedNews.objects.create(User=self.user, News=saved_article)
        url = reverse('briefly:saved_articles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample News")
        print("\n---\nSUCCESS: test_saved_articles \n---")

    def test_remove_saved_article(self):
        self.client.login(username="testuser", password="testpassword")
        saved_article = NewsArticle.objects.create(
            Title="Sample News",
            Content="Sample content",
            Source="SampleSource",
            Category=self.category
        )
        saved_news = SavedNews.objects.create(User=self.user, News=saved_article)
        url = reverse('briefly:remove_saved_article')
        form_data = {
            'article_id': saved_article.NewsID,
            'user_id': self.user.id
        }
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(SavedNews.objects.filter(User=self.user, News=saved_article).exists())
        print("\n---\nSUCCESS: test_remove_saved_article \n---")
    