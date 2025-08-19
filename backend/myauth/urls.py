from django.urls import path

from . import views


urlpatterns = [
    path('users/login', views.LoginView.as_view(), name='users_login'),
    path('token/refresh/', views.CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('users', views.RegistrationView.as_view(), name='users_registration'),
    path('users/logout', views.LogoutView.as_view(), name='users_logout'),
    path('user', views.UserView.as_view(), name='get_or_update_user'),
]
