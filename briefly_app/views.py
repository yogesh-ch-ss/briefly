from django.shortcuts import render, redirect
from django.http import HttpResponse
from briefly_app.forms import BrieflyUserSignupForm, BrieflyUserLoginForm, CategoryForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from briefly_app.models import UserCategory

# Signup, Login, Logout, Signout
# check if user is authenticated or not

def user_signup(request):
    # if user is authenticated, redirect to top_page
    if request.user.is_authenticated:
        return redirect('briefly:top_page')
    if request.method == 'POST':
        user_signup_form = BrieflyUserSignupForm(data=request.POST)
        if user_signup_form.is_valid():
            user = user_signup_form.save()            
            user.set_password(user.password)
            user.save()
            print(user)
            # when the sign up is successful, redirect to login page
            return redirect('briefly:user_login')
        else:
            print(user_signup_form.errors)
    else:
        user_signup_form = BrieflyUserSignupForm()
    return render(request, 'signup.html', {
        'user_signup_form': user_signup_form,
        'type' : 'signup',
        })

def user_login(request):
    # if user is authenticated, redirect to top_page
    if request.user.is_authenticated:
        return redirect('briefly:top_page')
    if request.method == 'POST':
        user_login_form = BrieflyUserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            username = user_login_form.cleaned_data['username']
            password = user_login_form.cleaned_data['password']
            print(username, password)
            user = authenticate(username=username, password=password)
            print(user)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('briefly:top_page')
                else:
                    return HttpResponse("Your account is disabled.")
            else:
                return HttpResponse("Invalid login details.")
        else:
            print(user_login_form.errors)
            return redirect('briefly:top_page')
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
        user_signup_form = BrieflyUserSignupForm(request.POST, instance=user)
        if user_signup_form.is_valid():
            if user_signup_form.cleaned_data['username'] != user.username:
                user.username = user_signup_form.cleaned_data['username']
            if user_signup_form.cleaned_data['email'] != user.email:
                user.email = user_signup_form.cleaned_data['email']
            if user_signup_form.cleaned_data['country'] != user.country:
                user.country = user_signup_form.cleaned_data['country']
            user.save()
            # login user with new credential
            user = authenticate(email=user.email, password=user.password)
            login(request, user)
    else:
        user_signup_form = BrieflyUserSignupForm(instance=user)
    return render(request, 'user_profile.html', {
        'type' : 'update',
        'user_signup_form': user_signup_form
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