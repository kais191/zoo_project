from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('create/', views.blog_post_create, name='create_post'),
    path('<int:post_pk>/comment/', views.add_comment, name='add_comment'),
    path('<int:post_pk>/like/', views.like_post, name='like_post'),
    path('signup/', views.signup, name='signup'),
    path('about/', views.about_us, name='about_us'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('add_post/', views.add_post, name='add_post'),
    path('about/', views.about_us, name='about_us'), 
    
    
    
]

