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

def signup(request):
    # if user is authenticated, redirect to top_page
    if request.user.is_authenticated:
        return redirect('briefly:top_page')
    if request.method == 'POST':
        user_signup_form = BrieflyUserSignupForm(data=request.POST)
        if user_signup_form.is_valid():
            user = user_signup_form.save()            
            user.set_password(user.password)
            user.save()
            # when the sign up is successful, redirect to login page
            return redirect('briefly:login')
        else:
            print(user_signup_form.errors)
    else:
        user_signup_form = BrieflyUserSignupForm()
    return render(request, 'signup.html', {'user_signup_form': user_signup_form})

def login(request):
    # if user is authenticated, redirect to top_page
    if request.user.is_authenticated:
        return redirect('briefly:top_page')
    if request.method == 'POST':
        user_login_form = BrieflyUserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            email = user_login_form.cleaned_data['email']
            password = user_login_form.cleaned_data['password']
            user = authenticate(email=email, password=password)
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
    else:
        user_login_form = BrieflyUserLoginForm()
        return render(request, 'login.html', {'user_login_form': user_login_form})

# !!!need to implement it in user profile page
@require_POST
@login_required
def logout(request):
    logout(request)
    return redirect('briefly:top_page')

# !!!need to implement it in user profile page
@login_required
@require_POST
def delete_account(request):
    if request.user.is_authenticated:
        request.user.delete()
    return redirect('briefly:top_page')

# choose and update category
# to choose category, user must be logged in
@login_required
def category_preference(request):
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

#views
#02/17/2025 Yongwoo - Deleted template_views, incorporated into views.
#Planning to remove 'template'
def index(request):
    return render(request, './template_index.html')

def top_page(request):
    return render(request, './template_top_page.html')

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