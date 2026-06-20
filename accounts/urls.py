from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/delete/', views.delete_account, name='delete_account'),
    path('search/', views.search_users, name='search_users'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('stats/<str:username>/', views.user_stats, name='user_stats'),
    path('followers/', views.followers_list, name='followers_list'),
    path('following/', views.following_list, name='following_list'),
]