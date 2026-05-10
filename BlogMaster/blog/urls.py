from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.articles, name='articles'),
    path('myarticles/', views.myarticles, name='myarticles'),
    path('article/add/', views.addarticle, name='addarticle'),
    path('article/edit/<int:article_id>/', views.editarticle, name='editarticle'),
    path('article/delete/<int:article_id>/', views.deletearticle, name='deletearticle'),
    path('article/<int:article_id>/', views.article, name='article'),
    path('comment/add/<int:article_id>/', views.commentadd, name='commentadd'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/<str:user_name>/', views.profile, name='profile')
]