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

class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('NewsID', 'Title', 'Category', 'Url', 'Date', 'Region', 'Source')
    fields = ('Title', 'Category', 'Url', 'Date', 'Region', 'Source')  # Ensure Date is included
    # readonly_fields = ('Date',)  


class ViewedNewsAdmin(admin.ModelAdmin):
    list_display = ('User', 'News')

class SavedNewsAdmin(admin.ModelAdmin):
    list_display = ('User', 'News')

admin.site.register(ViewedNews, ViewedNewsAdmin)
admin.site.register(SavedNews, SavedNewsAdmin)
admin.site.register(BrieflyUser, BrieflyUserAdmin) 
admin.site.register(Category)
admin.site.register(UserCategory)
admin.site.register(NewsArticle, NewsArticleAdmin)
