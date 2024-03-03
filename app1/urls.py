# app1/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.LoginPage, name="login"),
    path("signup/", views.SignupPage, name="signup"),
    path("logout/", views.LogoutPage, name="logout"),
    path("user/", views.HomePage, name="home"),
    path("edit/", views.EditProfile, name="edit"),
    path("user/<str:username>", views.userprofile, name="username"),
    path("add_friend/", views.add_friend, name="add_friend"),
    path("accept_request/", views.accept_request, name="accept_request"),
    path("delete_friend/", views.delete_friend, name="delete_friend"),
    path("search/", views.search, name="search"),
    path("chat/<str:username>", views.chat, name="chat"),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("dashboard/leaderboard/", views.leaderboard, name="leaderboard"),


]
