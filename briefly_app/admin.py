from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import BrieflyUser, Category, UserCategory, NewsArticle, ViewedNews, SavedNews

admin.site.register(BrieflyUser, UserAdmin) 
admin.site.register(Category)
admin.site.register(UserCategory)
admin.site.register(NewsArticle)
admin.site.register(ViewedNews)
admin.site.register(SavedNews)