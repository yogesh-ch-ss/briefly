from django.urls import path
from . import views

app_name = 'briefly'
urlpatterns = [
    path('', views.top_page, name='top_page'),
    # signup, login, logout, signout, profile_setting
    path('accounts/signup', views.signup, name='signup'),
    path('accounts/login', views.login, name='login'),
    path('accounts/logout', views.logout, name='logout'),
    path('accounts/delete', views.delete_account, name='delete_account'),
    # path('accounts/profile_setting', views.profile_setting, name='profile_setting'),
    path('accounts/profile_setting/category_preference', views.category_preference, name='category_preference'),
    # views
    # path('template_login', views.login, name='login'),
    path('template_headlines', views.headlines, name='headlines'),
    # path('template_login/template_signup', views.signup, name='sign_up'),
    path('template_headlines/template_add_category', views.add_category, name='add_category'),
    path('template_headlines/template_view_article', views.view_article, name='view_article'),
]
