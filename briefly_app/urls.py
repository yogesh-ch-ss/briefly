from django.urls import path
from . import views
#API Integration with .views
from .views import fetch_news

app_name = 'briefly'
urlpatterns = [
    path('', views.top_page, name='top_page'),
    # signup, login, logout, signout, profile_setting
    path('accounts/signup', views.user_signup, name='user_signup'),
    path('accounts/login', views.user_login, name='user_login'),
    path('accounts/logout', views.user_logout, name='user_logout'),
    path('accounts/delete', views.user_delete_account, name='user_delete_account'),
    path('accounts/profile_setting', views.user_profile_setting, name='user_profile_setting'),
    path('accounts/user_profile_setting/category_preference', views.user_category_preference, name='user_category_preference'),
    # views
    # path('template_login', views.login, name='login'),
    path('template_headlines', views.headlines, name='headlines'),
    # path('template_login/template_signup', views.signup, name='sign_up'),
    path('template_headlines/template_add_category', views.add_category, name='add_category'),
    path('template_headlines/template_view_article', views.view_article, name='view_article'),
    #sample endpoint
    path('api/news', fetch_news, name='fetch_news'),
]
