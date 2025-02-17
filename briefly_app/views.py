from django.shortcuts import render, redirect
from django.http import HttpResponse

#views
#02/17/2025 Yongwoo - Deleted template_views, incorporated into views.
  #Planning to remove 'template'
def index(request):
    return render(request, './template_index.html')

def top_page(request):
    return render(request, './template_top_page.html')

def login(request):
    return render(request, './template_login.html')

def signup(request):
    return render(request, './template_signup.html')

def add_category(request):
    return render(request, './template_category.html')

def headlines(request):
    return render(request, './template_headlines.html')

def view_article(request):
    return render(request, './template_view_article.html')