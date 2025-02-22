from django.shortcuts import render, redirect
from django.http import HttpResponse
#Rest and News API integration into views
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from newsapi import NewsApiClient
from briefly_app.forms import BrieflyUserSignupForm, BrieflyUserLoginForm, CategoryForm, BrieflyUserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from briefly_app.models import Category, UserCategory

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
        user_categories = UserCategory.objects.filter(UserID=user).values_list('CategoryID__CategoryName', flat=True)
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
        
        UserCategory.objects.filter(UserID=user).delete()
        for category in categories:
            category, created = Category.objects.get_or_create(CategoryName=category)
            UserCategory.objects.create(UserID=user, CategoryID=category)
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

#views
#02/17/2025 Yongwoo - Deleted template_views, incorporated into views.
#Planning to remove 'template'
def index(request):
    return render(request, './template_index.html')

def top_page(request):
    user = get_authenticated_user(request)
    return render(request, './template_top_page.html', {'user': user})

# def login(request):
#     return render(request, './template_login.html')

# def signup(request):
#     return render(request, './template_signup.html')

def add_category(request):
    return render(request, './template_category.html')

def headlines(request):
    return render(request, './template_headlines.html')

def view_article(request):
    return render(request, './template_view_article.html')

#Sample API Call
@api_view(['GET'])
def fetch_news(request):
    newsapi = NewsApiClient(api_key='d837b10b971a49949f9887d5f216055b')
    
    top_headlines = newsapi.get_top_headlines(
        sources='CNN'
    )

    sample_everything = newsapi.get_everything(q='bitcoin')


    return Response(sample_everything)