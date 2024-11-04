from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('user_profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('proper_user_profile/<int:user_id>/', views.proper_user_profile, name='proper_user_profile'),
    path('search/', views.search, name='search'),
    path('results/', views.search_results, name='search_results'),
]