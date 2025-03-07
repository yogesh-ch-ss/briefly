from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from django.contrib.auth.models import AbstractUser # Django's built-in User model - Abstract Class
# By default, Django's User model (from django.contrib.auth.models) has these important fields:

# username (or email if configured)
# password (hashed)
# is_staff → Controls access to /admin; is_staff=False → Prevents access to /admin/
# is_superuser → Gives full admin rights; is_superuser=False → No admin privileges
# is_active → Controls account activation
COUNTRY_CHOICES = [
        ('ae', 'United Arab Emirates'), ('ar', 'Argentina'), ('at', 'Austria'), ('au', 'Australia'), 
        ('be', 'Belgium'), ('bg', 'Bulgaria'), ('br', 'Brazil'), ('ca', 'Canada'), ('ch', 'Switzerland'), 
        ('cn', 'China'), ('co', 'Colombia'), ('cz', 'Czech Republic'), ('de', 'Germany'), ('eg', 'Egypt'), 
        ('fr', 'France'), ('gb', 'United Kingdom'), ('gr', 'Greece'), ('hk', 'Hong Kong'), ('hu', 'Hungary'), 
        ('id', 'Indonesia'), ('ie', 'Ireland'), ('il', 'Israel'), ('in', 'India'), ('it', 'Italy'), 
        ('jp', 'Japan'), ('kr', 'South Korea'), ('lt', 'Lithuania'), ('lv', 'Latvia'), ('ma', 'Morocco'), 
        ('mx', 'Mexico'), ('my', 'Malaysia'), ('ng', 'Nigeria'), ('nl', 'Netherlands'), ('no', 'Norway'), 
        ('nz', 'New Zealand'), ('ph', 'Philippines'), ('pl', 'Poland'), ('pt', 'Portugal'), ('ro', 'Romania'), 
        ('rs', 'Serbia'), ('ru', 'Russia'), ('sa', 'Saudi Arabia'), ('se', 'Sweden'), ('sg', 'Singapore'), 
        ('si', 'Slovenia'), ('sk', 'Slovakia'), ('th', 'Thailand'), ('tr', 'Turkey'), ('tw', 'Taiwan'), 
        ('ua', 'Ukraine'), ('us', 'United States'), ('ve', 'Venezuela'), ('za', 'South Africa')
    ]

CATEGORY_CHOICES = [
        ('business', 'business'),
        ('entertainment', 'entertainment'),
        ('general', 'general'),
        ('health', 'health'),
        ('science', 'science'),
        ('sports', 'sports'),
        ('technology', 'technology'),
    ]

class BrieflyUser(AbstractUser):
    # List of Users who signup to Briefly.
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)
    class Meta:
        verbose_name_plural = "BrieflyUsers"

    def __str__(self):
        return self.username

class Category(models.Model):
    # List of Categories available for the user to choose from to receive news.
    # there are 7 categories in newsapi - business, entertainment, general, health, science, sports, technology
    CategoryName = models.CharField(max_length=20, choices=CATEGORY_CHOICES, unique=True)
    
    def clean(self):
        if self.CategoryName.lower() not in dict(CATEGORY_CHOICES):
            raise ValidationError(f"{self.CategoryName} is not a valid category.")
        
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        # return self.CategoryID
        return self.CategoryName
    

class UserCategory(models.Model):
    # User - Category mapping. Categories selected by the user.
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "UserCategories"

class NewsArticle(models.Model):
    # List of News Articles fetched from the API.
    NewsID = models.AutoField(primary_key=True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    Url = models.CharField(max_length=255, blank=True)
    Title = models.CharField(max_length=255)
    Date = models.DateField(auto_now_add=True)
    Content = models.TextField()
    Region = models.TextField(max_length=2, null=True)
    Source = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "NewsArticles"

    def __str__(self):
        # return self.NewsID
        return self.Title

class ViewedNews(models.Model):
    # User - NewsArticle mapping. NewsArticles read by the user.
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    News = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "ViewedNews"

class SavedNews(models.Model):
    # User - NewsArticle mapping. NewsArticles saved by the user.
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    News = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "SavedNews"

