from django.urls import path
from . import views
#API Integration with .views

app_name = 'briefly'
urlpatterns = [
    path('', views.top_page, name='top_page'),
    path('qa', views.qa, name='qa'),
    # signup, login, logout, signout, profile_setting
    path('accounts/signup', views.user_signup, name='user_signup'),
    path('accounts/login', views.user_login, name='user_login'),
    path('accounts/logout', views.user_logout, name='user_logout'),
    path('accounts/delete', views.user_delete_account, name='user_delete_account'),
    path('accounts/profile_setting', views.user_profile_setting, name='user_profile_setting'),
    # views
    # path('template_login', views.login, name='login'),
    path('template_headlines', views.headlines, name='headlines'),
    # path('template_login/template_signup', views.signup, name='sign_up'),
    path('template_headlines/template_add_category', views.add_category, name='add_category'),
    # path('template_headlines/template_view_article', views.view_article, name='view_article'),
    #sample endpoint
    path('api/news', views.fetch_news, name='fetch_news'),
    # path('api/news/day_headlines', name='fetch_news_day_headlines'),
    path('news/', views.get_user_news, name="user_news"),
    # saved articles
    path('view_article/<int:article_id>/', views.view_article, name='view_article'),
    path('save_article', views.save_article, name='save_article'),
    path('saved_articles', views.saved_articles, name='saved_articles'),
    path('remove_saved_article', views.remove_saved_article, name='remove_saved_article'),
    path('delete-unsaved-news/', views.delete_unsaved_news, name="delete_unsaved_news"),
]
