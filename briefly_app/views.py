from collections import defaultdict
from django.shortcuts import render, redirect
from django.http import HttpResponse
from briefly_app.forms import BrieflyUserSignupForm, BrieflyUserLoginForm, CategoryForm, BrieflyUserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from briefly_app.models import Category, SavedNews, UserCategory, BrieflyUser, NewsArticle, UserCategory
from django.db.models import F


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

#Rest and News API integration into views
from django.conf import settings
from briefly.settings import BASE_DIR
from rest_framework.response import Response
from rest_framework.decorators import api_view
from newsapi import NewsApiClient

import environ
import os
from pathlib import Path

# Setting up NEWS API
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))
NEWS_API_KEY = env("NEWS_API_KEY", default=None)
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

# Signup, Login, Logout, Signout
# check if user is authenticated or not
def user_signup(request):
    # if user is authenticated, redirect to top_page
    if request.user.is_authenticated:
        return redirect('briefly:top_page')
    if request.method == 'POST':
        user_signup_form = BrieflyUserSignupForm(data=request.POST)
        if user_signup_form.is_valid():
            user_signup_form.save()  # Save the user and related categories in one go
            print('User created')
            # when the sign up is successful, redirect to login page
            return redirect('briefly:user_login')
        else:
            print(user_signup_form.errors)
    else:
        user_signup_form = BrieflyUserSignupForm()
    return render(request, 'signup.html', {
        'user_signup_form': user_signup_form,
    })

def user_login(request):
    # if user is authenticated, redirect to top_page
    if request.user.is_authenticated:
        return redirect('briefly:top_page')
    if request.method == 'POST':        
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('briefly:top_page')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details.")
    else:
        user_login_form = BrieflyUserLoginForm()
        return render(request, 'login.html', {'user_login_form': user_login_form})

# !!!need to implement it in user profile page
@require_POST
@login_required
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        # redirect to top_page
        return redirect('briefly:top_page')
    return redirect('briefly:top_page')

# !!!need to implement it in user profile page
@login_required
@require_POST
def user_delete_account(request):
    if request.user.is_authenticated:
        request.user.delete()
    return redirect('briefly:top_page')

# choose and update category
# to choose category, user must be logged in
@login_required
def user_category_preference(request):
    user = request.user
    if request.method == 'POST':
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save(user=user)
            return redirect('briefly:top_page')
    else:
        user_categories = UserCategory.objects.filter(User=user).values_list('Category__CategoryName', flat=True)
        initial_data = {'categories': list(user_categories)}
        category_form = CategoryForm(initial=initial_data)
    return render(request, 'category_preference.html', {'category_form': category_form})


# get profile_setting page
@login_required
def user_profile_setting(request):
    user = request.user
    if request.method == 'POST':
        # get name, email, country, and categories from the form
        # not using is_valid() because the form is not valid when the user does not select any category
        username = request.POST.get('username')
        email = request.POST.get('email')
        country = request.POST.get('country')
        categories = request.POST.getlist('categories')
        print(categories)
        user.username = username
        user.email = email
        user.country = country
        user.save()
        
        UserCategory.objects.filter(User=user).delete()
        for category in categories:
            category, created = Category.objects.get_or_create(CategoryName=category)
            UserCategory.objects.create(User=user, Category=category)
        return redirect('briefly:user_profile_setting')
    else:
        user_profile_form = BrieflyUserProfileForm(instance=user)
        return render(request, 'user_profile.html', {
        'user_profile_form': user_profile_form
        })


# function to check if the user is authenticated
def get_authenticated_user(request):
    if request.user.is_authenticated:
        return request.user
    return None

# view saved articles separately to the headlines page
@login_required
def saved_articles(request):
    user = request.user
    if user:    
        # Get SavedNews objects for the user
        saved_articles = SavedNews.objects.filter(User=user)
        saved_articles = [saved_article.News for saved_article in saved_articles]
        # Get NewsArticle objects related to the SavedNews objects
        return render(request, 'saved_articles.html', {'saved_articles': saved_articles})
    else:
        return redirect('briefly:user_login')

@login_required
def view_article(request, article_id):
    try:
        article = NewsArticle.objects.get(NewsID=article_id)
        return render(request, './view_article.html', {
            'article': article,
            "type" : "saved_article"
            })
    except NewsArticle.DoesNotExist:
        return HttpResponse("Article not found.", status=404)

#views
#02/17/2025 Yongwoo - Deleted template_views, incorporated into views.
#Planning to remove 'template'
def index(request):
    return render(request, './template_index.html')

def top_page(request):
    user = get_authenticated_user(request)
    random_article = NewsArticle.objects.order_by('?').first()
    return render(request, './template_top_page.html', {
        'user': user,
        'article': random_article
    })

# def login(request):
#     return render(request, './template_login.html')

# def signup(request):
#     return render(request, './template_signup.html')

def add_category(request):
    return render(request, './template_category.html')

def headlines(request):
    return render(request, './template_headlines.html')



#Sample API Call
@api_view(['GET'])
def fetch_news(request):
    
    # top_headlines = newsapi.get_top_headlines(
    #     sources='CNN'
    # )

    sample_query = 'bitcoin'
    # sample_everything = newsapi.get_everything(q=sample_query)
    # return Response(sample_everything)

    sample_top_headlines = newsapi.get_top_headlines()
    return Response(sample_top_headlines)

@api_view(['GET'])
def fetch_news_day_headlines(request):
    user = request.user

    # Get categories selected by the user
    user_categories = UserCategory.objects.filter(User=user).values_list("Category", flat=True)

    if not user_categories:
        return Response({"message": "No categories selected"}, status=400)

    # Fetch news articles that match the user’s categories
    articles = NewsArticle.objects.filter(Category__in=user_categories).values(
        "Title", "Date", "Content", "Source"
    )

    return Response({"articles": list(articles)})

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_user_news(request, username):

#     if request.user.username != username:
#         return Response({"error": "Unauthorized access. You can only fetch your own news."}, status=403)
    
#     try:
#         # Get the user
#         user = BrieflyUser.objects.get(username=username)
#         print(user)
#         # Get all categories the user is subscribed to
#         user_categories = UserCategory.objects.filter(User=user)
#         print("User Categories:", user_categories)

#         # Extract category names properly
#         category_names = user_categories.values_list('Category__CategoryName', flat=True)
#         print("Category Names:", list(category_names))  # Debugging

#         # Get the corresponding categories
#         categories = Category.objects.filter(CategoryName__in=category_names)
#         print("Categories:", categories)

#         # print("All News Articles:", list(NewsArticle.objects.all().values("Title", "Category_id", "Category__CategoryName")))

#         # Fetch news articles related to those categories
#         # news_articles = NewsArticle.objects.filter(Category__in=categories).values(
#         #     "Title", "Category__CategoryName", "Date", "Content", "Source"
#         # )
#         news_articles = NewsArticle.objects.filter(Category__in=categories).annotate(
#             CategoryName=F("Category__CategoryName")
#             ).values("Title", "CategoryName", "Date", "Content", "Source")
        
#         print("News Articles:", news_articles)
#         # return Response({"news": list(news_articles)})

#         context = {
#             "username": username,
#             "news": list(news_articles),
#         }
#         return render(request, "headlines.html", context)
    
#     except BrieflyUser.DoesNotExist:
#         return Response({"error": f"User '{username}' does not exist."}, status=404)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_news(request, username):
    if request.user.username != username:
        return Response({"error": "Unauthorized access. You can only fetch your own news."}, status=403)

    try:
        # Get the user
        user = BrieflyUser.objects.get(username=username)

        # Get all categories the user is subscribed to
        user_categories = UserCategory.objects.filter(User=user)
        category_names = user_categories.values_list('Category__CategoryName', flat=True)

        # Get the corresponding categories
        categories = Category.objects.filter(CategoryName__in=category_names)

        # Fetch news articles related to those categories
        news_articles = NewsArticle.objects.filter(Category__in=categories).annotate(
            CategoryName=F("Category__CategoryName")
        ).values("Title", "CategoryName", "Date", "Content", "Source")

        # **Group articles by category**
        grouped_news = defaultdict(list)
        for article in news_articles:
            grouped_news[article["CategoryName"]].append(article)

        context = {
            "username": username,
            "grouped_news": dict(grouped_news),  # Convert defaultdict to regular dict
        }
        return Response(context)
        # return render(request, "headlines.html", context)
    
    except BrieflyUser.DoesNotExist:
        return Response({"error": f"User '{username}' does not exist."}, status=404)