from . import views
from django.urls import path

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("user_manage/", views.user_manage_role, name="user_manage_role"),
]