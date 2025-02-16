from django.urls import path
from . import views, template_views

app_name = 'briefly'
urlpatterns = [
    path('', template_views.index, name='index'),
    path('template_top_page', template_views.top_page, name='top_page'),
    path('template_login', template_views.login, name='login'),
    path('template_add_category', template_views.add_category, name='add_category'),
    path('template_headlines', template_views.headlines, name='headlines'),
    path('template_view_article', template_views.view_article, name='view_article'),

]
