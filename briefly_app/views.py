from django.shortcuts import render, redirect
from django.http import HttpResponse
#Rest and News API integration into views
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from newsapi import NewsApiClient
import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

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

#Sample API Call
@api_view(['GET'])
def fetch_news(request):
    env = environ.Env()
    env.read_env(os.path.join(BASE_DIR, '.env'))
    NEWS_API_KEY = env("NEWS_API_KEY", default=None)
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
    
    top_headlines = newsapi.get_top_headlines(
        sources='CNN'
    )

    sample_query = 'bitcoin'
    sample_everything = newsapi.get_everything(q=sample_query)


    return Response(sample_everything)