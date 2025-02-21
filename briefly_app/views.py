from django.shortcuts import render, redirect
from django.http import HttpResponse
#Rest and News API integration into views
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from newsapi import NewsApiClient

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
    newsapi = NewsApiClient(api_key='d837b10b971a49949f9887d5f216055b')
    
    top_headlines = newsapi.get_top_headlines(
        sources='CNN'
    )

    sample_query = 'bitcoin'
    sample_everything = newsapi.get_everything(q=sample_query)


    return Response(sample_everything)