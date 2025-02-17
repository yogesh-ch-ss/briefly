from django.urls import path
from . import views

app_name = 'briefly'
urlpatterns = [
    path('', views.top_page, name='top_page'),
    path('template_login', views.login, name='login'),
    path('template_headlines', views.headlines, name='headlines'),

    path('template_login/template_signup', views.signup, name='sign_up'),
    path('template_headlines/template_add_category', views.add_category, name='add_category'),
    path('template_headlines/template_view_article', views.view_article, name='view_article'),
]
