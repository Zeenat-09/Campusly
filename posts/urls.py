from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create/', views.post_create, name='post_create'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('<int:pk>/like/', views.post_like, name='post_like'),
    path('<int:pk>/comment/', views.post_comment, name='post_comment'),
    path('<int:pk>/reshare/', views.post_reshare, name='post_reshare'),
]