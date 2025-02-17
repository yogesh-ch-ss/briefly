from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import BrieflyUser, Category, UserCategory, NewsArticle, ViewedNews, SavedNews

class BrieflyUserAdmin(UserAdmin):
    model = BrieflyUser
    fieldsets = UserAdmin.fieldsets + (  # Add the 'Country' field
        ("Additional Info", {"fields": ("country",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (  # Include 'Country' when adding a new user
        ("Additional Info", {"fields": ("country",)}),
    )


admin.site.register(BrieflyUser, BrieflyUserAdmin) 
admin.site.register(Category)
admin.site.register(UserCategory)
admin.site.register(NewsArticle)
admin.site.register(ViewedNews)
admin.site.register(SavedNews)