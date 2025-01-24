from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('book-ticket/', views.book_ticket, name='book_ticket'),
    path('add-post/', views.add_post, name='add_post'),
]
