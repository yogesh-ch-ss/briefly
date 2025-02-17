from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractUser # Django's built-in User model - Abstract Class
# By default, Django's User model (from django.contrib.auth.models) has these important fields:

# username (or email if configured)
# password (hashed)
# is_staff → Controls access to /admin; is_staff=False → Prevents access to /admin/
# is_superuser → Gives full admin rights; is_superuser=False → No admin privileges
# is_active → Controls account activation

class BrieflyUser(AbstractUser):
    # List of Users who signup to Briefly.
    country = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "BrieflyUsers"

    def __str__(self):
        return self.username

class Category(models.Model):
    # List of Categories available for the user to choose from to receive news.
    CategoryID = models.AutoField(primary_key=True)
    CategoryName = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.CategoryID
    

class UserCategory(models.Model):
    # User - Category mapping. Categories selected by the user.
    UserID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    CategoryID = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "UserCategories"

class NewsArticle(models.Model):
    # List of News Articles fetched from the API.
    NewsID = models.AutoField(primary_key=True)
    CategoryID = models.ForeignKey(Category, on_delete=models.CASCADE)
    Title = models.CharField(max_length=255)
    Date = models.DateField(auto_now_add=True)
    Content = models.TextField()
    Source = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "NewsArticles"

    def __str__(self):
        return self.NewsID

class ViewedNews(models.Model):
    # User - NewsArticle mapping. NewsArticles read by the user.
    UserID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    NewsID = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "ViewedNews"

class SavedNews(models.Model):
    # User - NewsArticle mapping. NewsArticles saved by the user.
    UserID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    NewsID = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "SavedNews"

