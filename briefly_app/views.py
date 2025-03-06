from collections import defaultdict
from django.shortcuts import render, redirect
from django.http import HttpResponse
from briefly_app.forms import BrieflyUserSignupForm, BrieflyUserLoginForm, BrieflyUserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from briefly_app.models import Category, SavedNews, UserCategory, BrieflyUser, NewsArticle, UserCategory
from django.db.models import F

#Rest and News API integration into views
from django.conf import settings
from briefly.settings import BASE_DIR
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from newsapi import NewsApiClient
from django.shortcuts import render
import json
import requests

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
                try:
                    #API call (check corresponding method implemenation)
                    fetch_news(user)
                except Exception as e:
                    print(f"Error fetching news: {e}")
                return redirect('briefly:user_news')
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

@login_required
def user_profile_setting(request):
    user = request.user
    if request.method == 'POST':
        # Pass both request.POST and the user instance to the form
        user_profile_form = BrieflyUserProfileForm(data=request.POST, instance=user)
        
        # Check if the form is valid
        if user_profile_form.is_valid():
            # Extract cleaned data
            username = user_profile_form.cleaned_data['username']
            email = user_profile_form.cleaned_data['email']
            country = user_profile_form.cleaned_data['country']
            selected_categories = user_profile_form.cleaned_data['categories']

            # Save user fields
            user.username = username
            user.email = email
            user.country = country
            user.save()
            
            UserCategory.objects.filter(User=user).delete()
            for category_name in selected_categories:
                category_obj, created = Category.objects.get_or_create(CategoryName=category_name)
                UserCategory.objects.create(User=user, Category=category_obj)
            return redirect('briefly:user_profile_setting')
        else:
            # If form is invalid (e.g., no category selected), re-render with errors
            return render(request, 'user_profile.html', {
                'user_profile_form': user_profile_form
            })
    else:
        # Populate form with initial data for GET requests
        user_profile_form = BrieflyUserProfileForm(instance=user)
        return render(request, 'user_profile.html', {
            'user_profile_form': user_profile_form
        })

# function to check if the user is authenticated
def get_authenticated_user(request):
    if request.user.is_authenticated:
        return request.user
    return None


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

@require_POST
@login_required
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        # redirect to top_page
        return redirect('briefly:top_page')
    return redirect('briefly:top_page')

@login_required
@require_POST
def user_delete_account(request):
    if request.user.is_authenticated:
        request.user.delete()
    return redirect('briefly:top_page')

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
        user.username = username
        user.email = email
        user.country = country
        user.save()

        if len(categories) == 0:
            return render(request, 'user_profile.html', {
                'user_profile_form': BrieflyUserProfileForm(instance=user),
                'error': 'You must select at least one category'
            })
        
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


<<<<<<< HEAD
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

@require_POST
@login_required
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        # redirect to top_page
        return redirect('briefly:top_page')
    return redirect('briefly:top_page')

@login_required
@require_POST
def user_delete_account(request):
    if request.user.is_authenticated:
        request.user.delete()
    return redirect('briefly:top_page')

@login_required
def user_profile_setting(request):
    user = request.user
    if request.method == 'POST':
        # Pass both request.POST and the user instance to the form
        user_profile_form = BrieflyUserProfileForm(data=request.POST, instance=user)
        
        # Check if the form is valid
        if user_profile_form.is_valid():
            # Extract cleaned data
            username = user_profile_form.cleaned_data['username']
            email = user_profile_form.cleaned_data['email']
            country = user_profile_form.cleaned_data['country']
            selected_categories = user_profile_form.cleaned_data['categories']

            # Save user fields
            user.username = username
            user.email = email
            user.country = country
            user.save()
            
            UserCategory.objects.filter(User=user).delete()
            for category_name in selected_categories:
                category_obj, created = Category.objects.get_or_create(CategoryName=category_name)
                UserCategory.objects.create(User=user, Category=category_obj)
            return redirect('briefly:user_profile_setting')
        else:
            # If form is invalid (e.g., no category selected), re-render with errors
            return render(request, 'user_profile.html', {
                'user_profile_form': user_profile_form
            })
    else:
        # Populate form with initial data for GET requests
        user_profile_form = BrieflyUserProfileForm(instance=user)
        return render(request, 'user_profile.html', {
            'user_profile_form': user_profile_form
        })

# function to check if the user is authenticated
def get_authenticated_user(request):
    if request.user.is_authenticated:
        return request.user
    return None


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

@require_POST
@login_required
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        # redirect to top_page
        return redirect('briefly:top_page')
    return redirect('briefly:top_page')

@login_required
@require_POST
def user_delete_account(request):
    if request.user.is_authenticated:
        request.user.delete()
    return redirect('briefly:top_page')

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
        user.username = username
        user.email = email
        user.country = country
        user.save()

        if len(categories) == 0:
            return render(request, 'user_profile.html', {
                'user_profile_form': BrieflyUserProfileForm(instance=user),
                'error': 'You must select at least one category'
            })
        
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
def saved_articles(request, response_type="html"):
    user = request.user
    if user:    
        # Get SavedNews objects for the user
        saved_articles = SavedNews.objects.filter(User=user)
        saved_articles = [saved_article.News for saved_article in saved_articles]
        # Get NewsArticle objects related to the SavedNews objects
        if response_type != "html":
            return Response({"saved_articles": list(saved_articles)})
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
    if user and user.is_authenticated:
        try:
        #API call (check corresponding method implemenation)
            fetch_news(user)
        except Exception as e:
            print(f"Error fetching news: {e}")
        return redirect('briefly:user_news')

    random_article = NewsArticle.objects.order_by('?').first()
    return render(request, './top_page.html', {
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


#NOT USED, LEFT FOR DOCUMENTATION PURPOSES
#Fetch Articles from API call (x5 times for each user login)
# @api_view(['GET'])
# def fetch_news(request):
#     news_data = newsapi.get_top_headlines(category='general')
#     # #directory for JSON
#     SUB_DIR = os.path.join(os.path.dirname(__file__), 'news_data')
#     os.makedirs(SUB_DIR, exist_ok=True)
#     JSON_FILE_PATH = os.path.join(SUB_DIR, 'news_data.json')

#     with open(JSON_FILE_PATH, 'w', encoding='utf-8') as json_file:
#         json.dump(news_data, json_file, ensure_ascii=False, indent=4)
    
#     return Response(news_data)

#Fetch News into a JSON file, populate database for each category
def fetch_news(user):
    try:
        # Get user's category preferences
        user_categories = UserCategory.objects.filter(User=user)
        
        #Handler for user error, shouldn't trigger unless user has selected no categories
        if not user_categories.exists():
            print(f"No categories selected for user {user.username}")
            return False
        
        #Array for User Data
        news_data = []
        
        # Fetch news for each of the user's categories
        for user_category in user_categories:
            category_name = user_category.Category.CategoryName
            try:
                # Make API call to News API, assign to api_response
                api_response = newsapi.get_top_headlines(
                    category=category_name,
                    country=user.country
                )
                #Print statement to flag the category name as it goes along
                print(category_name)
                
                if api_response["status"] == "ok" and "articles" in api_response:
                    # Extract articles
                    articles = api_response["articles"]
                    news_data.extend(articles)
                    category_obj = user_category.Category
                    #iterator to save only up to 5 articles per category
                    i = 0
                    # Save each article to the database
                    for article in articles:
                        if i >= 5: break
                        # Extract article data with fallbacks, makes URL the unique identifier, don't populate if article already exists
                        # (Models has been modified to take URL attribute as unique)
                        title = article.get('title', 'No title')
                        url = article.get('url')
                        content = article.get('content')
                        if not content:
                            #1st fallback for null content
                            content = article.get('description')
                            #2nd fallback for null content
                        if not content:
                            content = "No Preview Content Available: Click on Link to view Original Article"
                        source_name = article.get('source', {}).get('name', 'Unknown source')
                        
                        # Check for duplicates before saving
                        if not NewsArticle.objects.filter(Title=title).exists():
                            NewsArticle.objects.create(
                                Category=category_obj,
                                Title=title,
                                Url=url,
                                Content=content,
                                Source=source_name,
                                Region=user.country
                            )
                        i += 1
            except Exception as e:
                print(f"Error fetching news for category {category_name}: {e}")
                continue
        
        # Save to JSON file if needed
        SUB_DIR = os.path.join(os.path.dirname(__file__), 'news_data')
        os.makedirs(SUB_DIR, exist_ok=True)
        JSON_FILE_PATH = os.path.join(SUB_DIR, f'news_data.json')
        
        with open(JSON_FILE_PATH, 'w', encoding='utf-8') as json_file:
            json.dump(news_data, json_file, ensure_ascii=False, indent=4)
        
        print(f"Successfully fetched {len(news_data)} news articles for user {user.username}")
        return True
        
    except Exception as e:
        print(f"Error in fetch_news: {e}")
        return False

#Gets User's News AND Saved News from Models
# @api_view(['GET'])
# def get_user_news(request, username):
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

#         print("All News Articles:", list(NewsArticle.objects.all().values("Title", "Category_id", "Category__CategoryName")))

#         # Fetch news articles related to those categories
#         news_articles = NewsArticle.objects.filter(Category__in=categories).values(
#             "Title", "Date", "Content", "Source"
#         )
#         print("News Articles:", news_articles)
#         return Response({"news": list(news_articles)})
    
#     except BrieflyUser.DoesNotExist:
#         return Response({"error": f"User '{username}' does not exist."}, status=404)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
@login_required
def get_user_news(request):
    # if request.user.username != username:
    #     return Response({"error": "Unauthorized access. You can only fetch your own news."}, status=403)

    try:
        # Get the user
        # user = BrieflyUser.objects.get(username=request.u)
        user = request.user

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

        saved_articles_response = saved_articles(request, response_type="json")

        if isinstance(saved_articles_response, Response):
            saved_articles_data = saved_articles_response.data.get("saved_articles", [])
        else:
            saved_articles_data = []
        
        grouped_news["Saved News"] = saved_articles_data

        context = {
            "username": user.username,
            "grouped_news": dict(grouped_news),  # grouped news contains "saved_articles" as a category
        }
        # return Response(context)
        return render(request, "headlines.html", context)
    
    except BrieflyUser.DoesNotExist:
        return Response({"error": f"User '{user.username}' does not exist."}, status=404)