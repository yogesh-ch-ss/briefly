from django.urls import path
from . import views
#API Integration with .views
from .views import fetch_news, fetch_news_day_headlines

app_name = 'briefly'
urlpatterns = [
    path('', views.top_page, name='top_page'),
    path('template_login', views.login, name='login'),
    path('template_headlines', views.headlines, name='headlines'),

    path('template_login/template_signup', views.signup, name='sign_up'),
    path('template_headlines/template_add_category', views.add_category, name='add_category'),
    path('template_headlines/template_view_article', views.view_article, name='view_article'),
    #sample endpoint
    path('api/news', fetch_news, name='fetch_news'),
    path('api/news/day_headlines', fetch_news_day_headlines, name='fetch_news_day_headlines'),
]
